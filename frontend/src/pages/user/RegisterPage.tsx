import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Eye, EyeOff } from "lucide-react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useRegister } from "../../hooks";
import { 
  Button, 
  Input, 
  Checkbox,
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../../components/ui";
import type { AuthPage } from "../../components/auth/AuthRouter";

const registerSchema = z.object({
  username: z.string().min(2, { message: "Username must be at least 2 characters" }),
  email: z.string().email({ message: "Please enter a valid email address" }),
  password: z.string().min(8, { message: "Password must be at least 8 characters" }),
  confirmPassword: z.string(),
  agreeToTerms: z.boolean().refine(val => val === true, { message: "You must agree to the terms and conditions" }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type RegisterFormValues = z.infer<typeof registerSchema>;

interface RegisterPageProps {
  onNavigate?: (page: AuthPage) => void;
}

export const RegisterPage: React.FC<RegisterPageProps> = ({ onNavigate }) => {
  usePageInstructions("register");
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const { register, isLoading, error } = useRegister();

  const form = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      agreeToTerms: false,
    },
  });

  const onSubmit = async (data: RegisterFormValues) => {
    try {
      await register({
        username: data.username,
        email: data.email,
        password: data.password,
      });
      // Navigation happens automatically via App.tsx when isAuthenticated becomes true
    } catch (error) {
      // Error is handled by the hook and stored in error state
    }
  };

  return (
    <div className="relative min-h-screen bg-background">
      {/* Floating Chess Pieces - Enhanced with better spacing */}
      <div className="bg-overlay">
        <div className="hidden md:block bg-chess-piece text-2xl lg:text-3xl xl:text-4xl chess-piece-color-primary-30 absolute top-16 left-8 animate-pulse">♛</div>
        <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-accent-25 absolute top-28 right-12 animation-delay-400">♞</div>
        <div className="hidden md:block bg-chess-piece text-2xl lg:text-3xl xl:text-4xl chess-piece-color-primary-20 absolute bottom-44 left-20 animation-delay-800">♜</div>
        <div className="hidden md:block bg-chess-piece text-3xl lg:text-4xl xl:text-5xl chess-piece-color-foreground-15 absolute bottom-12 right-16 animation-delay-1200">♝</div>
        <div className="hidden lg:block bg-chess-piece text-xl chess-piece-color-muted absolute top-1/5 left-2 animation-delay-600">♟</div>
        <div className="hidden lg:block bg-chess-piece text-xl chess-piece-color-muted absolute bottom-1/4 right-4 animation-delay-1000">♟</div>
        <div className="hidden xl:block bg-chess-piece text-2xl chess-piece-color-accent-20 absolute top-2/3 left-6 animation-delay-200">♙</div>
        <div className="hidden xl:block bg-chess-piece text-2xl chess-piece-color-primary-15 absolute top-1/3 right-8 animation-delay-1400">♘</div>
      </div>

      <div className="flex items-center justify-center min-h-screen p-4">
        <div className="w-full max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl">
          <div className="card-gaming glass-hover p-6 sm:p-8 md:p-10 lg:p-12">
            {/* Header */}
            <div className="text-center mb-8 lg:mb-10">
              <div className="text-6xl sm:text-7xl lg:text-8xl xl:text-9xl mb-4 animate-pulse">♔</div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-3 tracking-tight">Join Master Chess Training</h1>
              <p className="text-base lg:text-lg xl:text-xl text-muted-foreground font-medium">Create your account to begin your journey</p>
              <div className="flex justify-center space-x-2 mt-3 text-xl sm:text-2xl lg:text-3xl opacity-60">
                <span>♚</span><span>♛</span><span>♜</span><span>♝</span><span>♞</span><span>♟</span>
              </div>
              {error && (
                <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}
            </div>

            {/* Register Form */}
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6 lg:space-y-8">
                {/* Username Field */}
                <FormField
                  control={form.control}
                  name="username"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Username</FormLabel>
                      <FormControl>
                        <Input
                          type="text"
                          placeholder="Choose a username"
                          autoComplete="username"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

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
                          placeholder="Enter your email"
                          autoComplete="email"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Password Field */}
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <div className="relative">
                          <Input
                            type={showPassword ? "text" : "password"}
                            placeholder="Create a password"
                            autoComplete="new-password"
                            className="pr-10"
                            {...field}
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors duration-200"
                          >
                            {showPassword ? (
                              <EyeOff className="h-4 w-4" />
                            ) : (
                              <Eye className="h-4 w-4" />
                            )}
                          </button>
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Confirm Password Field */}
                <FormField
                  control={form.control}
                  name="confirmPassword"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Confirm Password</FormLabel>
                      <FormControl>
                        <div className="relative">
                          <Input
                            type={showConfirmPassword ? "text" : "password"}
                            placeholder="Confirm your password"
                            autoComplete="new-password"
                            className="pr-10"
                            {...field}
                          />
                          <button
                            type="button"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors duration-200"
                          >
                            {showConfirmPassword ? (
                              <EyeOff className="h-4 w-4" />
                            ) : (
                              <Eye className="h-4 w-4" />
                            )}
                          </button>
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Terms and Conditions */}
                <FormField
                  control={form.control}
                  name="agreeToTerms"
                  render={({ field }) => (
                    <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                      <FormControl>
                        <Checkbox
                          checked={field.value}
                          onChange={(e) => field.onChange(e.target.checked)}
                          className="w-4 h-4 mt-1"
                        />
                      </FormControl>
                      <div className="space-y-1 leading-none">
                        <FormLabel className="text-xs text-muted-foreground font-normal">
                          I agree to the{" "}
                          <Button variant="link" className="p-0 h-auto text-xs text-primary hover:text-primary/80">
                            Terms of Service
                          </Button>
                          {" "}and{" "}
                          <Button variant="link" className="p-0 h-auto text-xs text-primary hover:text-primary/80">
                            Privacy Policy
                          </Button>
                        </FormLabel>
                        <FormMessage />
                      </div>
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
                        <span className="text-sm">Creating Account...</span>
                      </div>
                    ) : (
                      <span className="text-sm">Create Account</span>
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


            {/* Sign In Link */}
            <div className="mt-6 text-center">
              <p className="text-xs text-muted-foreground">
                Already have an account?{" "}
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