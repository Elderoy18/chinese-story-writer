"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { NotebookPen } from "lucide-react";
import { useSession } from "@/lib/auth-client";
import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuLabel, DropdownMenuTrigger } from "./ui/dropdown-menu";
import { Avatar, AvatarFallback } from "./ui/avatar";
import SignOutButton from "./sign-out-btn";

export default function Navbar(){
    const {data: session} = useSession();
    return(
        <nav className="border-b border-gray-200 bg-white">
            <div className="container mx-auto flex h-16 items-centerpx-4 justify-between">
                <Link href="/" className="flex items-center gap-2 text-xl font-semibold text-primary">
                    <NotebookPen />
                    Chinese Storyteller
                </Link>
                <div className="flex items-center gap-4">
                    
                    {session?.user ? (
                        <>
                            <Link href="/dashboard">
                                <Button
                                variant="ghost"
                                className="text-gray-700 hover:text-black"
                                >
                                    Dashboard
                                </Button>
                            </Link>
                            <DropdownMenu>
                                <DropdownMenuTrigger>
                                    <Button 
                                    variant="ghost"
                                    className="relative h-8 w-8 rounded-full"
                                    >
                                        <Avatar className="h-8 w-8">
                                            <AvatarFallback className="bg-primary">
                                                {session.user.name[0].toUpperCase()}
                                            </AvatarFallback>
                                        </Avatar>
                                    </Button>
                                </DropdownMenuTrigger>

                                <DropdownMenuContent className="w-47" align="end">
                                    <DropdownMenuGroup>
                                        <DropdownMenuLabel className="font-normal">
                                            <div className="flex flex-col space-y-1">
                                                <p className="text-sm font-medium leading-none">
                                                    {session.user.name}
                                                </p>
                                                <p className="text-xs leading-none text-muted-foreground">
                                                    {session.user.email}
                                                </p>
                                            </div>
                                        </DropdownMenuLabel>
                                    </DropdownMenuGroup>
                                    <SignOutButton />
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </>
                    ) : (
                    <>
                        <Link href="/sign-in">
                            <Button className="text-gray-900 hover:bg-primary/90">
                                Log In
                            </Button>
                        </Link>
                        <Link href="/sign-up">
                            <Button className="text-gray-900 hover:bg-primary/90">
                                Sign Up
                            </Button>
                        </Link>
                    </>)}
                </div>
            </div>
        </nav>
    );
}