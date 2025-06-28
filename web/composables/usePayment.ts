export const usePayment = () => {
  const openRazorpay = (order: {
    id: string;
    key: string;
    amount: number;
    currency: string;
    name?: string;
    description?: string;
    prefill?: {
      name?: string;
      email?: string;
      contact?: string;
    };
  }, handlePaymentCompletion) => {
    const options = {
      key: order.key,
      amount: order.amount,
      currency: order.currency,
      name: order.name || "DeepCite",
      description: order.description || "Payment",
      order_id: order.id,
      handler: function (response: any) {
        // Send `response.razorpay_payment_id` and `response.razorpay_signature`
        // to backend for verification
        handlePaymentCompletion(order.id, response.razorpay_payment_id, response.razorpay_signature)
      },
      prefill: order.prefill || {},
    };

    const rzp = new (window as any).Razorpay(options);
    rzp.open();
  };

  return { openRazorpay };
};
