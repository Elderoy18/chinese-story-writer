"use client";

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp, placeholderEmail } from "@/lib/auth-client";

export default function SignUp(){
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
            // Username + password only; Better Auth's required name and email are filled
            // from the username (the email is a hidden placeholder, see lib/auth-client.ts).
            const name = username.trim();
            const result = await signUp.email({
                name,
                username: name,
                email: placeholderEmail(name),
                password,
            });

            if(result.error){
                const code = result.error.code ?? "";
                setError(
                    code === "USERNAME_IS_ALREADY_TAKEN" || code === "USER_ALREADY_EXISTS"
                        ? "That username is already taken -- please choose another."
                        : code === "INVALID_USERNAME"
                            ? "Usernames can only use letters, numbers, _ and ."
                            : result.error.message ?? "Failed to sign up"
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
                        Sign Up
                    </CardTitle>
                    <CardDescription className="text-gray-600">
                        Create an account to start your story
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
                            placeholder="R2A_shennong"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            minLength={3}
                            maxLength={30}
                            pattern="[A-Za-z0-9_.]+"
                            className="border-gray-300 focus:border-primary focus:ring-primary">
                            </Input>
                            <p className="text-xs text-gray-500">3-30 letters, numbers, _ or . -- remember it to sign in.</p>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password" className="text-gray-700">
                                Password
                            </Label>
                            <Input
                            id="password"
                            type="password"
                            autoComplete="new-password"
                            placeholder="changbaicao123"
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
                            {loading ? "Creating account..." : "Sign Up"}
                        </Button>
                        <p className="text-center text-sm text-gray-600">
                            Already have an account? <Link href="/sign-in">Sign In</Link>
                        </p>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
