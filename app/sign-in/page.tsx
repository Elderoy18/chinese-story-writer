"use client";

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "@/lib/auth-client";

export default function SignIn(){
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const router = useRouter();

    async function handleSubmit(e: React.FormEvent){
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const id = username.trim();
            // Accounts created before usernames existed sign in with their email.
            const result = id.includes("@")
                ? await signIn.email({ email: id, password })
                : await signIn.username({ username: id, password });

            if(result.error){
                setError(
                    result.error.status === 401 || result.error.code === "INVALID_USERNAME_OR_PASSWORD"
                        ? "Wrong username or password."
                        : result.error.message ?? "Failed to sign in"
                );
            }else{
                router.push("/dashboard");
            }
        }catch(err){
            setError("An unexpected error occured");
        }finally{
            setLoading(false);
        }
    }


    return(
        <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-white p-4">
            <Card className="w-full max-w-md border-gray-200 shadow-lg">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl font-bold text-black">
                        Sign In
                    </CardTitle>
                    <CardDescription className="text-gray-600">
                        Enter your credentials to access your account
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <CardContent className="space-y-4">
                        {error && (
                        <div className="rounded-md bg-destructive/15 p-3 text-sm text-destructive">
                            {error}
                        </div>
                        )}
                        <div className="space-y-2">
                            <Label htmlFor="username" className="text-gray-700">
                                Username
                            </Label>
                            <Input
                            id="username"
                            type="text"
                            autoComplete="username"
                            placeholder="lily_wang"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            className="border-gray-300 focus:border-primary focus:ring-primary">
                            </Input>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password" className="text-gray-700">
                                Password
                            </Label>
                            <Input
                            id="password"
                            type="password"
                            autoComplete="current-password"
                            placeholder="your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={8}
                            className="border-gray-300 focus:border-primary focus:ring-primary">
                            </Input>
                        </div>
                    </CardContent>
                    <CardFooter className="flex flex-col space-y-4">
                        <Button
                        type="submit"
                        className="w-full bg-primary hover:bg-primary/90"
                        disabled={loading}>
                            {loading ? "Signing in..." : "Sign In"}
                        </Button>
                        <p className="text-center text-sm text-gray-600">
                            Don&apos;t have an account? <Link href="/sign-up">Sign Up</Link>
                        </p>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
