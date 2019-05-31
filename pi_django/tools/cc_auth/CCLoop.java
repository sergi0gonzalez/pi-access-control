import pt.gov.cartaodecidadao.*;
import java.io.*;
import java.net.*;
import java.nio.charset.Charset;


// javac  -cp ".:pteidlibj.jar" CCLoop.java
// java -Djava.library.path="/usr/local/lib" -cp ".:pteidlibj.jar" CCLoop

public class CCLoop
{
	
	public static void main(String[] args) {
		
		try {
			System.loadLibrary("pteidlibj");	
		} catch (UnsatisfiedLinkError e) 
		{
			System.err.println("Native code library failed to load. \n" + e);
			System.exit(1);
		}
		
		try {
			  ServerSocket welcomeSocket = new ServerSocket(5555);
			  
			  while (true)
			  {
				  Socket connectionSocket = welcomeSocket.accept();
				  System.out.println("Connection accepted...");
				  BufferedReader inFromClient = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
				  DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
				  String clientWord = inFromClient.readLine();
				  System.out.println(clientWord);
				  if(clientWord.equals("query")) 
				  {
						System.out.println("received query...");
						String message = "null";
						   
						PTEID_ReaderSet.initSDK();
						PTEID_EIDCard card;
						PTEID_EId eid;
						PTEID_ReaderContext context;
						PTEID_ReaderSet readerSet;
						readerSet = PTEID_ReaderSet.instance();
						for( int i=0; i < readerSet.readerCount(); i++)
						{
							System.out.println("Reader is present");
							context = readerSet.getReaderByNum(i);
							if (context.isCardPresent())
							{
								System.out.println("Card is present");
								card = context.getEIDCard();
								eid = card.getID();
								String nome = eid.getGivenName();
								String ultimo_nome = eid.getSurname();
								String nome_inteiro = nome + " " + ultimo_nome;
								String id = eid.getCivilianIdNumber();
								PTEID_Photo photoObj = eid.getPhotoObj();
								PTEID_ByteArray ppng = photoObj.getphoto();
								//ppng.writeToFile("test.png");
								byte[] image_bytes = ppng.GetBytes();
								String image_hex = CCLoop.bytesToHex(image_bytes);
								
								message = "{\"name\":\"" + nome_inteiro + "\",\"civilian_id\":\"" + id + "\",\"image_bytes\":\"" + image_hex + "\"}";
								System.out.println("Generated response...");
							}
						}
						PTEID_ReaderSet.releaseSDK();
						outToClient.write(message.getBytes(Charset.forName("UTF-8"))); 
							    
				  }
			  }
		}
		catch(Exception ex) {
			ex.printStackTrace();
		}
		
		
	}
	
	public static String bytesToHex(byte[] bytes) {
		    char[] hexArray = "0123456789ABCDEF".toCharArray();
			char[] hexChars = new char[bytes.length * 2];
			for ( int j = 0; j < bytes.length; j++ ) {
				int v = bytes[j] & 0xFF;
				hexChars[j * 2] = hexArray[v >>> 4];
				hexChars[j * 2 + 1] = hexArray[v & 0x0F];
			}
			return new String(hexChars);
	}	
}
