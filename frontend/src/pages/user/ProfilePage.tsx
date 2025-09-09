import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Eye, EyeOff, User, Mail, Calendar, Trophy, Target, Settings, LogOut, Edit2, Save, X } from "lucide-react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useProfile, useLogout, useUser } from "../../hooks";
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
import { AuthLayout } from "../../components/auth/AuthLayout";

const profileSchema = z.object({
  username: z.string().min(2, { message: "Username must be at least 2 characters" }),
  email: z.string().email({ message: "Please enter a valid email address" }),
});

const changePasswordSchema = z.object({
  currentPassword: z.string().min(1, { message: "Current password is required" }),
  newPassword: z.string().min(8, { message: "Password must be at least 8 characters" }),
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type ProfileFormValues = z.infer<typeof profileSchema>;
type ChangePasswordFormValues = z.infer<typeof changePasswordSchema>;

export const ProfilePage: React.FC = () => {
  usePageInstructions("profile");
  
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  const { user } = useUser();
  const { updateProfile, changePassword, isLoading, error, clearError } = useProfile();
  const logout = useLogout();

  const profileForm = useForm<ProfileFormValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      username: user?.username || "",
      email: user?.email || "",
    },
  });

  const passwordForm = useForm<ChangePasswordFormValues>({
    resolver: zodResolver(changePasswordSchema),
    defaultValues: {
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
    },
  });

  const onUpdateProfile = async (data: ProfileFormValues) => {
    try {
      await updateProfile(data);
      setIsEditingProfile(false);
      clearError();
    } catch (error) {
      // Error is handled by the hook
    }
  };

  const onChangePassword = async (data: ChangePasswordFormValues) => {
    try {
      await changePassword({
        currentPassword: data.currentPassword,
        newPassword: data.newPassword,
      });
      setIsChangingPassword(false);
      passwordForm.reset();
      clearError();
    } catch (error) {
      // Error is handled by the hook
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (!user) {
    return (
      <AuthLayout>
        <div className="text-center">
          <div className="text-6xl sm:text-7xl lg:text-8xl xl:text-9xl mb-4 animate-pulse">♔</div>
          <p className="text-base lg:text-lg xl:text-xl text-muted-foreground font-medium">Loading profile...</p>
          <div className="flex justify-center space-x-2 mt-3 text-xl sm:text-2xl lg:text-3xl opacity-60">
            <span>♚</span><span>♛</span><span>♜</span><span>♝</span><span>♞</span><span>♟</span>
          </div>
        </div>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout>
      <div className="w-full max-w-md md:max-w-2xl lg:max-w-4xl xl:max-w-5xl space-y-6 mx-auto">
          {/* Profile Header */}
          <div className="card-gaming glass-hover p-6 sm:p-8 md:p-10 lg:p-12">
            <div className="text-center mb-6">
              <div className="text-6xl sm:text-7xl lg:text-8xl xl:text-9xl mb-4 animate-pulse">♔</div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-3 tracking-tight">Master Chess Training</h1>
              <p className="text-base lg:text-lg xl:text-xl text-muted-foreground font-medium">Your Profile</p>
              <div className="flex justify-center space-x-2 mt-3 text-xl sm:text-2xl lg:text-3xl opacity-60">
                <span>♚</span><span>♛</span><span>♜</span><span>♝</span><span>♞</span><span>♟</span>
              </div>
              {error && (
                <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}
            </div>

            {/* Profile Information */}
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex items-center space-x-3 p-3 bg-muted/20 rounded-lg">
                  <User className="w-4 h-4 text-primary" />
                  <div>
                    <p className="text-xs text-muted-foreground">Username</p>
                    <p className="text-sm font-medium">{user.username}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-muted/20 rounded-lg">
                  <Mail className="w-4 h-4 text-primary" />
                  <div>
                    <p className="text-xs text-muted-foreground">Email</p>
                    <p className="text-sm font-medium">{user.email}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-muted/20 rounded-lg">
                  <Trophy className="w-4 h-4 text-primary" />
                  <div>
                    <p className="text-xs text-muted-foreground">Chess ELO</p>
                    <p className="text-sm font-medium">{user.chess_elo || 1000}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-muted/20 rounded-lg">
                  <Target className="w-4 h-4 text-primary" />
                  <div>
                    <p className="text-xs text-muted-foreground">Puzzle Rating</p>
                    <p className="text-sm font-medium">{user.puzzle_rating || 1000}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3 p-3 bg-muted/20 rounded-lg">
                <Calendar className="w-4 h-4 text-primary" />
                <div>
                  <p className="text-xs text-muted-foreground">Member Since</p>
                  <p className="text-sm font-medium">
                    {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'}
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-3">
              <Button
                onClick={() => setIsEditingProfile(true)}
                variant="secondary"
                size="sm"
                className="w-full py-2.5"
              >
                <Edit2 className="w-4 h-4 mr-2" />
                <span className="text-sm">Edit Profile</span>
              </Button>
              <Button
                onClick={() => setIsChangingPassword(true)}
                variant="secondary"
                size="sm"
                className="w-full py-2.5"
              >
                <Settings className="w-4 h-4 mr-2" />
                <span className="text-sm">Change Password</span>
              </Button>
              <Button
                onClick={handleLogout}
                variant="destructive"
                size="sm"
                className="w-full py-2.5"
              >
                <LogOut className="w-4 h-4 mr-2" />
                <span className="text-sm">Sign Out</span>
              </Button>
            </div>
          </div>

          {/* Edit Profile Modal */}
          {isEditingProfile && (
            <div className="card-gaming glass-hover p-6 sm:p-8 md:p-10 lg:p-12">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-foreground">Edit Profile</h2>
                <Button
                  onClick={() => setIsEditingProfile(false)}
                  variant="ghost"
                  size="sm"
                  className="p-2"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <Form {...profileForm}>
                <form onSubmit={profileForm.handleSubmit(onUpdateProfile)} className="space-y-4">
                  <FormField
                    control={profileForm.control}
                    name="username"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            type="text"
                            placeholder="Enter username"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={profileForm.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            type="email"
                            placeholder="Enter email"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex space-x-3 pt-2">
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="flex-1 py-2.5"
                      size="sm"
                    >
                      {isLoading ? (
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          <span className="text-sm">Saving...</span>
                        </div>
                      ) : (
                        <>
                          <Save className="w-4 h-4 mr-2" />
                          <span className="text-sm">Save Changes</span>
                        </>
                      )}
                    </Button>
                    <Button
                      type="button"
                      onClick={() => setIsEditingProfile(false)}
                      variant="outline"
                      className="flex-1 py-2.5"
                      size="sm"
                    >
                      <span className="text-sm">Cancel</span>
                    </Button>
                  </div>
                </form>
              </Form>
            </div>
          )}

          {/* Change Password Modal */}
          {isChangingPassword && (
            <div className="card-gaming glass-hover p-6 sm:p-8 md:p-10 lg:p-12">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-foreground">Change Password</h2>
                <Button
                  onClick={() => setIsChangingPassword(false)}
                  variant="ghost"
                  size="sm"
                  className="p-2"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <Form {...passwordForm}>
                <form onSubmit={passwordForm.handleSubmit(onChangePassword)} className="space-y-4">
                  <FormField
                    control={passwordForm.control}
                    name="currentPassword"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <div className="relative">
                            <Input
                              type={showCurrentPassword ? "text" : "password"}
                              placeholder="Enter current password"
                              className="pr-10"
                              {...field}
                            />
                            <button
                              type="button"
                              onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors duration-200"
                            >
                              {showCurrentPassword ? (
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

                  <FormField
                    control={passwordForm.control}
                    name="newPassword"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <div className="relative">
                            <Input
                              type={showNewPassword ? "text" : "password"}
                              placeholder="Enter new password"
                              className="pr-10"
                              {...field}
                            />
                            <button
                              type="button"
                              onClick={() => setShowNewPassword(!showNewPassword)}
                              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors duration-200"
                            >
                              {showNewPassword ? (
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

                  <FormField
                    control={passwordForm.control}
                    name="confirmPassword"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <div className="relative">
                            <Input
                              type={showConfirmPassword ? "text" : "password"}
                              placeholder="Confirm new password"
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

                  <div className="flex space-x-3 pt-2">
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="flex-1 py-2.5"
                      size="sm"
                    >
                      {isLoading ? (
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          <span className="text-sm">Changing...</span>
                        </div>
                      ) : (
                        <>
                          <Save className="w-4 h-4 mr-2" />
                          <span className="text-sm">Change Password</span>
                        </>
                      )}
                    </Button>
                    <Button
                      type="button"
                      onClick={() => setIsChangingPassword(false)}
                      variant="outline"
                      className="flex-1 py-2.5"
                      size="sm"
                    >
                      <span className="text-sm">Cancel</span>
                    </Button>
                  </div>
                </form>
              </Form>
            </div>
          )}
      </div>
    </AuthLayout>
  );
};