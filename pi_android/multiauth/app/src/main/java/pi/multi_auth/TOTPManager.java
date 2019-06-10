package pi.multi_auth;

import java.nio.ByteBuffer;
import java.security.GeneralSecurityException;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/**
 * <p>TOTP: Time-Based One-Time Password Algorithm
 *
 * <p>Bean to easily generate TOTP for 2 step authentication. Is <a href="http://tools.ietf.org/html/rfc6238">RFC6238</a>
 * compliant and it's default configuration is also compatible with <a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en">Google Authenticator</a>.
 *
 * <p>This allows for easy 2 step authentication integration with own service
 * without necessity to write own code generating application
 *
 * <p>TODO: Allow generation of backup codes
 *
 * @author Gregor "hrax" Magdolen
 * @version $Id$
 */
public class TOTPManager {

    private static final int[] DIGITS_POWER
            // 0  1   2    3     4      5       6        7         8
            = {1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000};

    /**
     * Default algorithm (Google Authenticator Compatible)
     */
    public static final String DEFAULT_ALGORITHM = "HmacSHA256";

    /**
     * Default time interval in seconds (Google Authenticator Compatible)
     */
    public static final int DEFAULT_INTERVAL = 30;

    /**
     * Default time interval steps to check into past for validity
     */
    public static final int DEFAULT_STEPS = 1;

    /**
     * Default code length (Google Authenticator Compatible)
     */
    public static final int DEFAULT_LENGTH = 8;

    /**
     * Default time 0 for the interval
     */
    public static final int DEFAULT_T0 = 0;

    private final String algorithm;

    private final int interval;

    private final int length;

    private final int steps;

    private final int t0;

    /**
     * Create default TOTP instance that is Google Authenticator compatible
     */
    public TOTPManager() {
        this(DEFAULT_ALGORITHM, DEFAULT_INTERVAL, DEFAULT_LENGTH, DEFAULT_STEPS, DEFAULT_T0);
    }

    /**
     * @param algorithm the algorithm to use; available HmacSHA1, HmacSHA256, HmacSHA512
     * @param interval the time interval in seconds to use
     */
    public TOTPManager(String algorithm, int interval) {
        this(algorithm, interval, DEFAULT_LENGTH, DEFAULT_STEPS, DEFAULT_T0);
    }

    /**
     * Create new TOTP instance with own time interval
     *
     * @param interval the time interval to use
     */
    public TOTPManager(int interval) {
        this(DEFAULT_ALGORITHM, interval, DEFAULT_LENGTH, DEFAULT_STEPS, DEFAULT_T0);
    }

    /**
     * @param interval the time interval in seconds to use
     * @param length the code length to use; must be between 1 and 8
     * @param steps the steps in history to validate code
     */
    public TOTPManager(int interval, int length, int steps) {
        this(DEFAULT_ALGORITHM, interval, length, steps, DEFAULT_T0);
    }

    /**
     * Create new TOTP instance with own configuration
     *
     * @param algorithm the algorithm to use; available HmacSHA1, HmacSHA256, HmacSHA512
     * @param interval the time interval in seconds to use
     * @param length the code length to use; must be between 1 and 8
     * @param steps the steps in history to validate code
     * @param t0 the time 0 to be used for interval
     */
    public TOTPManager(String algorithm, int interval, int length, int steps, int t0) {
        this.algorithm = algorithm;
        this.interval = Math.abs(interval);
        this.length = Math.abs(length);
        this.steps = Math.abs(steps);
        this.t0 = Math.abs(t0);

        if (length > DIGITS_POWER.length || length < 1) {
            throw new IllegalArgumentException("Length must be between 1 and 8");
        }
    }

    /**
     * @return the algorithm being used
     */
    public String getAlgorithm() {
        return algorithm;
    }

    /**
     * @return the interval being used
     */
    public int getInterval() {
        return interval;
    }

    /**
     * @return the length being used
     */
    public int getLength() {
        return length;
    }

    /**
     * @return the steps being used
     */
    public int getSteps() {
        return steps;
    }

    /**
     * @return the time 0 to be used for interval
     */
    public int getT0() {
        return t0;
    }


    public final String generate(byte[] secret) {
        return generateOTP(secret, getCurrentTimeInterval());
    }

    public final String generate(byte[] secret, long time) {
        return generateOTP(secret, getTimeInterval(time));
    }


    public final boolean validate(byte[] secret, String code) {
        return validate(secret, code, System.currentTimeMillis());
    }


    public final boolean validate(byte[] secret, String code, long time) {
        int steps = getSteps();
        long itvl = getTimeInterval(time);

        for (int i = 0; i <= steps; i++) {
            boolean result = validateOTP(secret, itvl - i, code);
            if (result) {
                return true;
            }
        }

        return false;
    }

    final String generateOTP(byte[] secret, long itvl) {
        byte[] text = ByteBuffer.allocate(8).putLong(itvl).array();
        byte[] hash = getShaHash(secret, text);

        int off = hash[hash.length-1] & 0xf;
        int bin = ((hash[off] & 0x7f) << 24) | ((hash[off + 1] & 0xff) << 16) | ((hash[off + 2] & 0xff) << 8) | (hash[off + 3] & 0xff);

        int otp = bin % DIGITS_POWER[getLength()];
        String result = Integer.toString(otp);
        while (result.length() < getLength()) {
            result = "0" + result;
        }
        return result;
    }

    final boolean validateOTP(byte[] secret, long itvl, String code) {
        String hash = generateOTP(secret, itvl);
        return hash.equals(code);
    }

    private byte[] getShaHash(byte[] key, byte[] text) {
        try {
            Mac mac = Mac.getInstance(getAlgorithm());
            SecretKeySpec spec = new SecretKeySpec(key, "RAW");
            mac.init(spec);
            return mac.doFinal(text);
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException(e);
        }
    }

    long getTimeInterval(long time) {
        return ((time / 1000) - getT0()) / getInterval();
    }

    long getCurrentTimeInterval() {
        return getTimeInterval(System.currentTimeMillis());
    }

}
