import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Eye, EyeOff } from "lucide-react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useLogin, useDemoLogin } from "../../hooks";
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
import { AuthLayout } from "../../components/auth/AuthLayout";
import { RegisterPageWrapper } from "./RegisterPageWrapper";
import { ForgotPasswordPageWrapper } from "./ForgotPasswordPageWrapper";
import { useAppStore } from "../../stores/appStore";
import type { AuthPage } from "../../components/auth/AuthRouter";

const loginSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email address" }),
  password: z.string().min(6, { message: "Password must be at least 6 characters" }),
  rememberMe: z.boolean(),
});

type LoginFormValues = z.infer<typeof loginSchema>;

interface LoginPageProps {
  onNavigate?: (page: AuthPage) => void;
}

export const LoginPage: React.FC<LoginPageProps> = () => {
  usePageInstructions("login");
  
  const currentChildPage = useAppStore((state) => state.currentChildPage);
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  
  // Handle child page navigation - pure store-based
  const handleNavigate = (page: AuthPage) => {
    if (page === 'register') {
      setCurrentChildPage('register');
    } else if (page === 'forgotPassword') {
      setCurrentChildPage('forgotPassword');
    } else if (page === 'login') {
      setCurrentChildPage(null);
    }
  };
  
  // Render child pages
  if (currentChildPage === 'register') {
    return <RegisterPageWrapper onNavigate={handleNavigate} />;
  }
  
  if (currentChildPage === 'forgotPassword') {
    return <ForgotPasswordPageWrapper onNavigate={handleNavigate} />;
  }
  
  return <LoginMainPage onNavigate={handleNavigate} />;
};

// Main login page component
const LoginMainPage: React.FC<{ onNavigate?: (page: AuthPage) => void }> = ({ onNavigate }) => {
  const [showPassword, setShowPassword] = useState(false);
  const { login, isLoading, error } = useLogin();
  const { loginWithDemo, isLoading: isDemoLoading } = useDemoLogin();

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
      rememberMe: false,
    },
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      await login({
        email: data.email,
        password: data.password,
      });
      // Navigation happens automatically via App.tsx when isAuthenticated becomes true
      // Note: rememberMe is handled by the client-side storage, not sent to API
    } catch (error) {
      // Error is handled by the hook and stored in error state
    }
  };

  const handleDemoLogin = async () => {
    try {
      await loginWithDemo();
      // Navigation happens automatically via App.tsx when isAuthenticated becomes true
    } catch (error) {
      // Error is handled by the hook and stored in error state
    }
  };

  return (
    <AuthLayout>
            {/* Header */}
            <div className="text-center mb-8 lg:mb-10">
              <div className="text-6xl sm:text-7xl lg:text-8xl xl:text-9xl mb-4 animate-pulse">♔</div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-3 tracking-tight">Master Chess Training</h1>
              <p className="text-base lg:text-lg xl:text-xl text-muted-foreground font-medium">Sign in to continue your chess journey</p>
              <div className="flex justify-center space-x-2 mt-3 text-xl sm:text-2xl lg:text-3xl opacity-60">
                <span>♚</span><span>♛</span><span>♜</span><span>♝</span><span>♞</span><span>♟</span>
              </div>
              {error && (
                <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}
            </div>

              {/* Login Form */}
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
                        <FormControl>
                          <div className="relative">
                            <Input
                              type={showPassword ? "text" : "password"}
                              placeholder="Enter your password"
                              autoComplete="current-password"
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

                  {/* Remember Me & Forgot Password */}
                  <div className="flex items-center justify-between text-xs">
                    <FormField
                      control={form.control}
                      name="rememberMe"
                      render={({ field }) => (
                        <FormItem className="flex flex-row items-center space-x-2 space-y-0">
                          <FormControl>
                            <Checkbox
                              checked={field.value}
                              onChange={(e) => field.onChange(e.target.checked)}
                              className="w-3 h-3"
                            />
                          </FormControl>
                          <FormLabel className="text-muted-foreground font-normal">
                            Remember
                          </FormLabel>
                        </FormItem>
                      )}
                    />
                    <Button
                      type="button"
                      onClick={() => onNavigate?.('forgotPassword')}
                      variant="link"
                      className="p-0 h-auto text-xs text-primary hover:text-primary/80"
                    >
                      Forgot password?
                    </Button>
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    disabled={isLoading || isDemoLoading}
                    className="w-full py-2.5"
                    size="sm"
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        <span className="text-sm">Signing in...</span>
                      </div>
                    ) : (
                      <span className="text-sm">Sign in</span>
                    )}
                  </Button>

                  {/* Demo Login Button */}
                  <Button
                    type="button"
                    onClick={handleDemoLogin}
                    disabled={isLoading || isDemoLoading}
                    variant="secondary"
                    className="w-full py-2.5"
                    size="sm"
                  >
                    {isDemoLoading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <div className="w-3 h-3 border-2 border-muted-foreground/30 border-t-muted-foreground rounded-full animate-spin" />
                        <span className="text-sm">Demo Login...</span>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center space-x-2">
                        <span className="text-lg">♔</span>
                        <span className="text-sm">Try Demo Account</span>
                      </div>
                    )}
                  </Button>
                </form>
              </Form>


              {/* Sign Up Link */}
              <div className="mt-6 text-center">
                <p className="text-xs text-muted-foreground">
                  Don't have an account?{" "}
                  <Button 
                    onClick={() => onNavigate?.('register')}
                    variant="link" 
                    className="p-0 h-auto text-xs text-primary hover:text-primary/80"
                  >
                    Sign up
                  </Button>
                </p>
              </div>
    </AuthLayout>
  );
};