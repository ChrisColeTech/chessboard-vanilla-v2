import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
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

interface ForgotPasswordPageProps {
  onNavigate?: (page: AuthPage) => void;
}

export const ForgotPasswordPage: React.FC<ForgotPasswordPageProps> = ({ onNavigate }) => {
  usePageInstructions("forgotPassword");
  
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
      <div className="relative min-h-screen bg-background">
        {/* Floating Chess Pieces - Enhanced with better spacing */}
        <div className="bg-overlay">
          <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-primary-30 absolute top-10 left-10 animate-pulse">♛</div>
          <div className="hidden md:block bg-chess-piece text-2xl lg:text-3xl xl:text-4xl chess-piece-color-accent-25 absolute top-36 right-14 animation-delay-400">♞</div>
          <div className="hidden md:block bg-chess-piece text-2xl lg:text-3xl xl:text-4xl chess-piece-color-primary-20 absolute bottom-36 left-24 animation-delay-800">♜</div>
          <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-foreground-15 absolute bottom-14 right-18 animation-delay-1200">♝</div>
          <div className="hidden lg:block bg-chess-piece text-xl chess-piece-color-muted absolute top-1/4 left-6 animation-delay-600">♟</div>
          <div className="hidden lg:block bg-chess-piece text-xl chess-piece-color-muted absolute bottom-1/3 right-10 animation-delay-1000">♟</div>
          <div className="hidden xl:block bg-chess-piece text-2xl chess-piece-color-accent-20 absolute top-1/2 left-4 animation-delay-200">♙</div>
          <div className="hidden xl:block bg-chess-piece text-2xl chess-piece-color-primary-15 absolute bottom-1/4 right-2 animation-delay-1400">♘</div>
        </div>

        <div className="flex items-center justify-center min-h-screen p-4">
          <div className="w-full max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl">
            <div className="card-gaming glass-hover p-6 sm:p-8 md:p-10 lg:p-12">
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
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-background">
      {/* Floating Chess Pieces - Enhanced with better spacing */}
      <div className="bg-overlay">
        <div className="hidden md:block bg-chess-piece text-2xl lg:text-3xl xl:text-4xl chess-piece-color-primary-30 absolute top-20 left-14 animate-pulse">♛</div>
        <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-accent-25 absolute top-24 right-10 animation-delay-400">♞</div>
        <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-primary-20 absolute bottom-48 left-18 animation-delay-800">♜</div>
        <div className="hidden md:block bg-chess-piece text-2xl lg:text-3xl xl:text-4xl chess-piece-color-foreground-15 absolute bottom-18 right-22 animation-delay-1200">♝</div>
        <div className="hidden lg:block bg-chess-piece text-xl chess-piece-color-muted absolute top-1/6 left-4 animation-delay-600">♟</div>
        <div className="hidden lg:block bg-chess-piece text-xl chess-piece-color-muted absolute bottom-1/5 right-6 animation-delay-1000">♟</div>
        <div className="hidden xl:block bg-chess-piece text-2xl chess-piece-color-accent-20 absolute top-3/5 left-8 animation-delay-200">♙</div>
        <div className="hidden xl:block bg-chess-piece text-2xl chess-piece-color-primary-15 absolute top-2/5 right-12 animation-delay-1400">♘</div>
      </div>

      <div className="flex items-center justify-center min-h-screen p-4">
        <div className="w-full max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl">
          <div className="card-gaming glass-hover p-6 sm:p-8 md:p-10 lg:p-12">
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
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6 lg:space-y-8">
                {/* Email Field */}
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
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
                <div className="flex flex-col sm:flex-row gap-3">
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

            {/* Back to Login */}
            <div className="mt-6 text-center">
              <p className="text-xs text-muted-foreground">
                Remember your password?{" "}
                <Button 
                  onClick={() => onNavigate?.('login')}
                  variant="link" 
                  className="p-0 h-auto text-xs text-primary hover:text-primary/80"
                >
                  Sign in
                </Button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};