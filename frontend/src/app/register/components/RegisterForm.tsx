"use client";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AuthClient } from "@/lib/auth/client";
import { UserCreate, User } from "@/lib/users/types";

const registerSchema = z.object({
  email: z.email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

type RegisterFormData = z.infer<typeof registerSchema>;

type RegisterFormProps = {
  handleRegisterSuccess: () => void;
};

export function RegisterForm({ handleRegisterSuccess }: RegisterFormProps) {
  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (registerForm: UserCreate) => AuthClient.register(registerForm),
    onSuccess: (user: User) => {
      handleRegisterSuccess();
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    mutate({
      email: data.email,
      password: data.password,
    });
  };

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-4"
        noValidate
      >
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
                  {...field}
                  disabled={isPending}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  type="password"
                  placeholder="Enter your password"
                  {...field}
                  disabled={isPending}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {isError && (
          <div className="text-sm text-destructive text-center">
            {error.message}
          </div>
        )}

        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? "Signing Up..." : "Sign Up"}
        </Button>
      </form>
    </Form>
  );
}
