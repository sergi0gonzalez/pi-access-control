import os
import pickle
import glob

# deletes a registered user from database
def delete_user():
    name = input("Enter name of the user:")



    user = db.pop(name, None)

    if user is not None:
        print('User ' + name + ' deleted successfully')
        # save the database

        [os.remove(path) for path in glob.glob('./voice_database/' + name + '/*')]
        os.removedirs('./voice_database/' + name)
        os.remove('./gmm_models/' + name + '.gmm')

    else:
        print('No such user !!')

if __name__ == '__main__':
    delete_user()
