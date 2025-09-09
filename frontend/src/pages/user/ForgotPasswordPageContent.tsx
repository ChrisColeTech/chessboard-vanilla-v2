import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useForgotPassword } from "../../hooks";
import { 
  Button, 
  Input,
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../../components/ui";
import type { AuthPage } from "../../components/auth/AuthRouter";

const forgotPasswordSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email address" }),
});

type ForgotPasswordFormValues = z.infer<typeof forgotPasswordSchema>;

interface ForgotPasswordPageContentProps {
  onNavigate?: (page: AuthPage) => void;
}

export const ForgotPasswordPageContent: React.FC<ForgotPasswordPageContentProps> = ({ onNavigate }) => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const { forgotPassword, isLoading, error } = useForgotPassword();

  const form = useForm<ForgotPasswordFormValues>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = async (data: ForgotPasswordFormValues) => {
    try {
      await forgotPassword(data.email);
      setIsSubmitted(true);
    } catch (error) {
      // Error is handled by the hook and stored in error state
    }
  };

  if (isSubmitted) {
    return (
      <>
        {/* Header */}
        <div className="text-center mb-6">
          <div className="text-6xl sm:text-7xl lg:text-8xl xl:text-9xl mb-4 animate-pulse">♔</div>
          <h1 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-3 tracking-tight">Master Chess Training</h1>
          <p className="text-base lg:text-lg xl:text-xl text-muted-foreground font-medium">We've sent password reset instructions to your email address</p>
          <div className="flex justify-center space-x-2 mt-3 text-xl sm:text-2xl lg:text-3xl opacity-60">
            <span>♚</span><span>♛</span><span>♜</span><span>♝</span><span>♞</span><span>♟</span>
          </div>
        </div>

        <div className="text-center space-y-4">
          <p className="text-sm text-muted-foreground">
            Didn't receive the email? Check your spam folder or try again.
          </p>
          <Button 
            onClick={() => setIsSubmitted(false)}
            variant="outline"
            className="w-full"
          >
            Send Another Email
          </Button>
          <Button 
            onClick={() => onNavigate?.('login')}
            variant="link" 
            className="w-full text-xs text-primary hover:text-primary/80"
          >
            Back to Sign In
          </Button>
        </div>
      </>
    );
  }

  return (
    <>
      {/* Header */}
      <div className="text-center mb-6">
        <div className="text-6xl sm:text-7xl lg:text-8xl xl:text-9xl mb-4 animate-pulse">♔</div>
        <h1 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-3 tracking-tight">Master Chess Training</h1>
        <p className="text-base lg:text-lg xl:text-xl text-muted-foreground font-medium">Enter your email to receive reset instructions</p>
        <div className="flex justify-center space-x-2 mt-3 text-xl sm:text-2xl lg:text-3xl opacity-60">
          <span>♚</span><span>♛</span><span>♜</span><span>♝</span><span>♞</span><span>♟</span>
        </div>
        {error && (
          <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}
      </div>

      {/* Forgot Password Form */}
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 sm:space-y-5 md:space-y-6">
          {/* Email Field */}
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <Input
                    type="email"
                    placeholder="Enter your email address"
                    autoComplete="email"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {/* Submit and Cancel Buttons */}
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 md:gap-4">
            <Button
              type="submit"
              disabled={isLoading}
              className="flex-1 py-2.5"
              size="sm"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span className="text-sm">Sending...</span>
                </div>
              ) : (
                <span className="text-sm">Send Reset Instructions</span>
              )}
            </Button>
            <Button
              type="button"
              onClick={() => onNavigate?.('login')}
              variant="outline"
              className="flex-1 py-2.5"
              size="sm"
            >
              <span className="text-sm">Cancel</span>
            </Button>
          </div>
        </form>
      </Form>

    </>
  );
};