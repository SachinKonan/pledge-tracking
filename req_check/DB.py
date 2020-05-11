import pyrebase
import functools

FIREBASE_CREDENTIALS = {
    "apiKey": "AIzaSyCRJp-MFY5YPoKwqJNsTgNzDThW3FWfDQo",
    "authDomain": "gtakpsi-rush.firebaseapp.com",
    "databaseURL": "https://gtakpsi-rush.firebaseio.com",
    "storageBucket": "gtakpsi-rush.appspot.com",
}

def default_removal(func):
    def recursiveRemove(iterable):
        if not(isinstance(iterable, list) or isinstance(iterable, dict)):
            return iterable
        else:
            if isinstance(iterable, list):
                del_ix = set()
                for i in range(0, len(iterable)):
                    if iterable[i] == 'default':
                        del_ix.add(i)
                    else:
                        iterable[i] = recursiveRemove(iterable[i])
                return [i for j, i in enumerate(iterable) if j not in del_ix]
            else:
                del_k = set()
                for i in iterable.keys():
                    if i == 'default':
                        del_k.add(i)
                    else:
                        iterable[i] = recursiveRemove(iterable[i])
                return {k:v for k,v in iterable.items() if k not in del_k}

    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, set):
            return result - {'default'}
        elif isinstance(result, list) or isinstance(result, dict):
            return recursiveRemove(result)
        else:
            return result
    return inner

class firebase:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(FIREBASE_CREDENTIALS)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()
        self.user = None

    @default_removal
    def __getitem__(self, items):
        return self.getChild(items).get().val()

    def getChild(self, items):
        if type(items) == str:
            return self.db.child(items)
        elif type(items) == tuple:
            last = self.db.child(items[0])
            for i in range(1, len(items)):
                if last is None:
                    return None
                last = last.child(items[i])
            return last

    def __setitem__(self, items, value):
        self.getChild(items).set(value)

    def getDict(self):
        return self.db.child().get().val()

class database:
    def __init__(self):
        self.db = firebase()

    def getMostRecentEmailToken(self):
        return self.db['rush_emails']['last_history_token']

    def getDatabase(self):
        return self.db.getDict()

    def getEmailTokens(self):
        return set(self.db['rush_emails', 'email_tokens'].values())

    def getPledgeEmails(self):
        return self.db['rush_emails', 'emails'].keys()

    def createDefaultUser(self, sender):
        self.db['rush_emails','emails', sender, 'default'] = {'From': 'default', 'Date': 'default', 'Subject': 'default', 'Body': 'default'}

    def addEmail(self, sender, date, emailId, historyToken, subject, body):
        if sender not in self.db['rush_emails', 'emails']:
            print('Sender not in database: %s' % (sender))
            self.createDefaultUser(sender)
        all_emails = self.db['rush_emails', 'emails', sender]
        self.db['rush_emails', 'emails', sender, len(all_emails) + 1] = {'From': sender, 'Date': date, 'Token': historyToken, 'Email_id': emailId, 'Subject': subject, 'Body': body}

    def addProcessedEmailToken(self, token):
        all_tokens = self.db['rush_emails', 'email_tokens']
        all_tokens[len(all_tokens) + 1] = token