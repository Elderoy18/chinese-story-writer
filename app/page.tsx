import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-white">
      <main>
        {/* Hero Section */}
        <section className="container mx-auto px-4py-32">
          <div className="mx-auto max-w-4xl text center">
            <h1 className="text-black mb-6 text-6xl font-bold">
              Learn Chinese Through Storytelling
            </h1>
            <p className="text-muted-foreground mb-10 text-xl">
              Watch Traditional Stories, Interact With Characters, Write Your Own
            </p>
            <div className="flex flex-col items-center gap-4">
              <button>
                Make an account
              </button>
              <p className="text-sm txt-muted-foreground">
                Watch your progress skyrocket!
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
