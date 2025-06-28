from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from billing.enums import PaymentStatus
from billing.models import APIPayment
from billing.serializers import APIPaymentSerializer


@extend_schema(exclude=True)
class APIPaymentViewSet(viewsets.ModelViewSet):
    queryset = APIPayment.objects.all()
    serializer_class = APIPaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the transaction first with user
        payment = serializer.save(user=self.request.user, status=PaymentStatus.INITIATED)

        # Create order after saving
        try:
            payment.create_order()
        except Exception as e:
            # Delete the object if order creation fails
            payment.delete()
            raise e

    def destroy(self, request, *args, **kwargs):
        return NotImplementedError()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='update-status')
    def update_status(self, request):
        order_id = request.data.get('order_id')
        payment_id = request.data.get('payment_id')
        signature = request.data.get('signature')
        payment = APIPayment.objects.get(order_id=order_id)

        if not payment_id or not signature:
            return Response({'error': 'payment_id and signature are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment.update_status(payment_id=payment_id, signature=signature)
            return Response({'status': 'success', 'transaction_status': payment.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
