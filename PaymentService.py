import mysql.connector


class PaymentService:
    notificationRestClient = NotificationRestClient()
    cbrRestClient = CbrRestClient()

    def __init__(self, feeRepository, userRepository):
        self.feeRepository = feeRepository
        self.userRepository = userRepository

    def processPayment(self, amount, currency, authToken):
        myconn = mysql.connector.connect(host="localhost", user="user", password="password",database="database")
        cur = myconn.cursor()

        amountInRub = amount * self.cbrRestClient.doRequest().getRates().get(currency.getCode())
        userId = AuthenticationService(authToken).getUsetId()
        user = self.userRepository.findUserById(userId)
        payment = Payment(amountInRub, user);
        paymentRepository(cur).save(payment)
        if amountInRub < 1000:
            fee = Fee(amountInRub * 0.015, user)
            cur.execute(self. feeRepository.save(fee))
        if amountInRub > 1000:
            fee = Fee(amountInRub * 0.01, user)
            cur.execute(self. feeRepository.save(fee))
        if amountInRub > 5000:
            fee = Fee(amountInRub * 0.005, user)
            cur.execute(self. feeRepository.save(fee))

        myconn.commit()
        try:
            self.notificationRestClient.notify(payment)
        except:
            pass


class paymentRepository:
    def __init__(cur):
        cur = cur

    def save(self, payment):
        self.cur.execute(self.getInsertQuery(payment.user.id, payment.amountInRub, payment.user.name))

    def getInsertQuery(self, userId, amount, userName):
        return f"""INSERT INTO payment (user_id, amount, user_name) VALUES ('{userId}','{amount}',{userName})"""

class FeeRepository:
    def save(self):
        return """INSERT INTO fee (user_id, fee) VALUES ('""" + fee.amountInRub + """','""" + fee.user.userId + """')"""
