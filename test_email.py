import yagmail

yag = yagmail.SMTP("working122614@gmail.com", "hsvjdfgnlzaqgqub")

yag.send(
    to="varshapeddireddy9@gmail.com",
    subject="Test Mail",
    contents="Testing email from Python"
)

print("Mail sent successfully")