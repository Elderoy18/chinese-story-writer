"use client";
import {Button} from "@/components/ui/button";
import { useState } from "react";
import Image from "next/image";

export default function ImageTabs(){
    const [activeTab, setActiveTab] = useState("write") // watch, write, interact
    return(
        <section className="border-t bg-white py-16">
            <div className="container mx-auto px-4">
                <div className="mx-auto max-w-6xl">
                    {/* Tabs */}
                    <div className="flex gap-2 justify-center mb-8">
                        <Button onClick={() => setActiveTab("watch")}
                            className={`rounded-lg px-6 py-3 text-sm font-medium transition-colors ${
                                activeTab === "watch"
                                ? "bg-primary text-white"
                                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                            }`}
                        >
                            Watch Traditional Stories
                        </Button>
                        <Button onClick={() => setActiveTab("write")}
                            className={`rounded-lg px-6 py-3 text-sm font-medium transition-colors ${
                                activeTab === "write"
                                ? "bg-primary text-white"
                                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                            }`}
                        >
                            Write Your Own
                        </Button>
                        <Button onClick={() => setActiveTab("interact")}
                            className={`rounded-lg px-6 py-3 text-sm font-medium transition-colors ${
                                activeTab === "interact"
                                ? "bg-primary text-white"
                                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                            }`}
                        >
                            Interact with Characters
                        </Button>
                    </div>
                    <div className="relative mx-auto max-w-5xl overflow-hidden rounded-lg border-gray-200 shadow-xl">
                        {activeTab === "watch" && (<Image 
                            src="/hero-images/houyi.png"
                            alt="Write Your Own"
                            width={1200}
                            height={800}
                        />)}

                        {activeTab === "write" && (<Image 
                            src="/hero-images/liujunning.png"
                            alt="Watch Traditional Stories"
                            width={1200}
                            height={800}
                        />)}

                        {activeTab === "interact" && (<Image 
                            src="/hero-images/shennong.png"
                            alt="Interact with Characters"
                            width={1200}
                            height={800}
                        />)}
                    </div>
                </div>
            </div>
        </section>

    );
}