docker build -t bezugly_task https://github.com/BezuglyR/Task2_ukr_Docker.net.git#main

Test Case Steps:
 1. Login into mail
 2. Send 15 mails to self mail(from step 1). Subject random 10 length string witch contains letters and numbers.
     Massage test is random 10 length string witch contains letters and numbers.
 3. Check if all 15 mails received(inbox)
 4. Collect subjects and massages text from mail main page into dict, where key=subject value=text
 5. Send collected info from dict to self mail, massage text format : "Received mail on theme {subject}
     with message: {massage text}. It contains {quantity letters in text} letters and {quantity numbers in text}
     numbers". In this format, must input for all 15 mails.
 6. Delete all mails except last one.
