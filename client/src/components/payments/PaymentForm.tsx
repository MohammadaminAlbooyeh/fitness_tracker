import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  CardElement,
  Elements,
  useStripe,
  useElements,
} from '@stripe/react-stripe-js';
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Alert,
  Paper,
  Container,
} from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { api } from '../../services/api';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLIC_KEY);

const PaymentForm: React.FC<{
  consultationId: number;
  professionalId: number;
  amount: number;
  onSuccess: () => void;
  onCancel: () => void;
}> = ({ consultationId, professionalId, amount, onSuccess, onCancel }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const { token } = useAuth();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);
    setError(null);

    try {
      // Create payment intent
      const { data: paymentIntent } = await api.post(
        '/payments/payment-intent',
        {
          consultation_id: consultationId,
          professional_id: professionalId,
          amount: amount,
          currency: 'USD'
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      // Confirm the payment with Stripe
      const card = elements.getElement(CardElement);
      if (!card) {
        throw new Error('Card element not found');
      }

      const { error: stripeError, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card,
      });

      if (stripeError) {
        throw new Error(stripeError.message);
      }

      // Confirm the payment with our backend
      await api.post(
        `/payments/${paymentIntent.payment_id}/confirm`,
        {
          payment_intent_id: paymentMethod.id
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      onSuccess();

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Payment failed');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Payment Details
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Amount: ${amount.toFixed(2)}
        </Typography>
      </Box>

      <Box
        sx={{
          border: '1px solid #e0e0e0',
          borderRadius: 1,
          p: 2,
          mb: 3,
          backgroundColor: '#f8f8f8'
        }}
      >
        <CardElement
          options={{
            style: {
              base: {
                fontSize: '16px',
                color: '#424770',
                '::placeholder': {
                  color: '#aab7c4',
                },
              },
              invalid: {
                color: '#9e2146',
              },
            },
          }}
        />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button
          type="button"
          onClick={onCancel}
          disabled={processing}
          variant="outlined"
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={!stripe || processing}
          variant="contained"
          color="primary"
        >
          {processing ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            `Pay $${amount.toFixed(2)}`
          )}
        </Button>
      </Box>
    </form>
  );
};

const PaymentFormWrapper: React.FC<{
  consultationId: number;
  professionalId: number;
  amount: number;
  onSuccess: () => void;
  onCancel: () => void;
}> = (props) => {
  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Elements stripe={stripePromise}>
          <PaymentForm {...props} />
        </Elements>
      </Paper>
    </Container>
  );
};

export default PaymentFormWrapper;