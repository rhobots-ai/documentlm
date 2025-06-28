import razorpay
from razorpay.errors import SignatureVerificationError, BadRequestError

from config import settings


class RazorpayService:

    def __init__(self):
        self.key = settings.RAZORPAY_KEY
        self.client = razorpay.Client(auth=(self.key, settings.RAZORPAY_SECRET))

    def create_customer(self, name, email, contact=None):
        try:
            data = {
                "name": name,
                "email": email,
                "contact": contact,
            }
            customer = self.client.customer.create(data=data)
            return customer['id']
        except BadRequestError:
            return self.get_customer(email)

    def get_customer(self, email: str):
        customers = self.client.customer.all()
        customer = list(filter(lambda c: c['email'] is not None and c['email'].lower() == email.lower(), customers['items']))
        return customer[0]['id'] if customer else None

    def create_invoice(self, receipt_id, customer_id, line_item_id, quantity, currency, invoice_date, notes=None):
        if notes is None:
            notes = {}
        data = {
            "type": "invoice",
            "date": invoice_date,
            "partial_payment": 0,
            "customer_id": customer_id,
            "line_items": [{
                "item_id": line_item_id,
                "quantity": quantity
            }],
            "invoice_number": str(receipt_id),
            "notes": notes,
            "sms_notify": 1,
            "email_notify": 1,
            "currency": currency
        }
        invoice = self.client.invoice.create(data=data)
        return invoice['id'], invoice['order_id'], invoice['short_url']

    def get_invoice(self, invoice_id):
        return self.client.invoice.fetch(invoice_id)

    def create_order(self, receipt_id, amount, currency, notes=None):
        if notes is None:
            notes = {}
        data = {
            "amount": amount,
            "currency": currency,
            "receipt": str(receipt_id),
            "notes": notes
        }
        order = self.client.order.create(data=data)
        return order['id']

    def create_subscription(self, plan_id, notes = None):
        if notes is None:
            notes = {}
        data = {
            'plan_id': plan_id,
            'customer_notify': False,
            'quantity': 1,
            'total_count': 60,
            'notes': notes
        }
        subscription = self.client.subscription.create(data=data)
        return subscription

    def update_subscription(self, subscription_id, options):
        self.client.subscription.edit(subscription_id, options)


    def verify_payment_signature(self, order_id, payment_id, signature):
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        return self.client.utility.verify_payment_signature(params_dict)

    def verify_invoice_signature(self, parameters):
        # {razorpay_payment_id: 'pay_M8pBohrkOsZ2WC', razorpay_invoice_id: 'inv_M8pBLnILtoj6z6', razorpay_invoice_status: 'paid', razorpay_invoice_receipt:
        # null, razorpay_signature: '8ff858ab7c03e18b37f227414fd8af4e602f2690a89220c49f3fddce25d15a36'}
        # if 'razorpay_payment_id' in parameters.keys() and 'razorpay_invoice_id' in parameters.keys() and 'razorpay_invoice_status' in parameters.keys():
        #     payment_id = str(parameters['razorpay_payment_id'])
        #     razorpay_invoice_id = str(parameters['razorpay_invoice_id'])
        #     payment_link_reference_id = str(parameters['payment_link_reference_id'])
        #     razorpay_invoice_status = str(parameters['razorpay_invoice_status'])
        #     razorpay_signature = str(parameters['razorpay_signature'])
        # else:
        #     return False
        #
        # msg = "{}|{}|{}".format(razorpay_invoice_id, razorpay_invoice_status, razorpay_payment_id)
        #
        # secret = str(parameters['secret']) if 'secret' in parameters.keys() else str(self.client.auth[1])
        #
        # return self.client.utility.verify_signature(msg, razorpay_signature, secret)
        pass

    def verify_webhook_signature(self, webhook_body, webhook_signature):
        try:
            return self.client.utility.verify_webhook_signature(webhook_body, webhook_signature, settings.RAZORPAY_WEBHOOK_SECRET_KEY)
        except SignatureVerificationError:
            return False

    def get_payment(self, payment_id):
        return self.client.payment.fetch(payment_id)

    def get_subscription(self, subscription_id):
        return self.client.subscription.fetch(subscription_id)

    def get_subscription_invoices(self, subscription_id):
        return self.client.invoice.all({'subscription_id': subscription_id})['items']

    def get_payments_by_order(self, order_id):
        return self.client.order.payments(order_id)
