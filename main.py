import webapp2, re, cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style>
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>User Signup</h1>
"""

form = """
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required/>
                        <span class="error">%(username_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required/>
                        <span class="error">%(password_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required/>
                        <span class="error">%(verify_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(email)s"/>
                        <span class="error">%(email_error)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(u):
    return USER_RE.match(u)

USER_PW = re.compile(r"^.{3,20}$")
def valid_password(p):
    return USER_PW.match(p)

USER_EM = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(e):
    return USER_EM.match(e)

def esc_html(s):
    return cgi.escape(s, quote=True)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", password="", verify="", email="",
        username_error="", password_error="", verify_error="", email_error=""):

        dictionary = {
            "username": esc_html(username),
            "username_error": username_error,
            "password": "",
            "password_error": password_error,
            "verify": "",
            "verify_error": verify_error,
            "email": esc_html(email),
            "email_error": email_error
        }

        content = page_header + form + page_footer
        self.response.out.write(content % dictionary)

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error = False

        username_error = ""
        if not valid_username(username):
            username_error = "Not a valid username."
            error = True

        password_error = ""
        if not valid_password(password):
            password_error = "Not a valid password."
            error = True

        verify_error = ""
        if not password==verify:
            verify_error = "Passwords do not match."
            error = True

        email_error = ""
        if email and not valid_email(email):
            email_error = "Not a valid email."

        if error:
            self.write_form(username, password, verify, email,
                username_error, password_error, verify_error, email_error)
        else:
            self.redirect("/welcome?username="+username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        welcome = "<h1>Welcome, " + username + "!</h1>"
        self.response.out.write(welcome)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
