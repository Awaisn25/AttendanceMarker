# from mailthon.envelope import Envelope
# from mailthon.enclosure import PlainText
# from mailthon import postman as postman_

# envelope = Envelope(
#     headers={
#         'Sender': 'sender <awaisnawaz2000@gmail.com>',
#         'To': 'mawais.ce41ceme@ce.ceme.edu.pk',
#         'Subject': 'Hello World!',
#     },
#     enclosure=[
#         PlainText('Hi!'),
#     ]
# )

# postman = postman_(
#     host='mail.google.com',
#     port=80,
#     force_tls=True,
#     auth=('awaisnawaz2000@gmail.com', 'awaisn@25'),
# )

# # response = postman.send(envelope)
# # print(postman, envelope)
# # print(response.message)
# # print(response.status_code)

# # if response.ok:
# #     print("OK! :)")

from mailthon import postman, email
p = postman(host='smtp.gmail.com', auth=('awaisnawaz2000@gmail.com', 'fbcabwnopmdugkhx'))
r = p.send(email(
        content=u'<p>This user is absent</p>',
        subject='Hello world',
        sender='Awais <awaisnawaz2000@gmail.com>',
        receivers=['awaisnawaz2000@gmail.com'],
    ))
assert r.ok
# print(r)
