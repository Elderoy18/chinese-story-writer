import ImageTabs from "@/components/image-tabs";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-white">
      <main className="flex-1">
        {/* Hero Section */}
        <section className="container mx-auto px-4 py-32">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-black mb-6 text-6xl font-bold">
              Learn Chinese Through Storytelling
            </h1>
            <p className="text-muted-foreground mb-10 text-xl">
              Watch Traditional Stories, Interact With Characters, Write Your Own
            </p>
            <div className="flex flex-col items-center gap-4">
              <Link href="/sign-up">
                <Button size="lg" className="h-12px-8 text-lg font-medium">
                  Get Started <ArrowRight className="ml-2"/>
                </Button>
              </Link>
                
              <p className="text-sm text-muted-foreground">
                Watch your progress skyrocket!
              </p>
            </div>
          </div>
        </section>

        {/* Hero Images Section with Tabs */}
        <ImageTabs />

      </main>
    </div>
  );
}
