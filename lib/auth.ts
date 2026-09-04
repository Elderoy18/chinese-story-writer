import dns from "dns";
dns.setServers(["1.1.1.1", "8.8.8.8"]);

import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { MongoClient } from "mongodb";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

// Cache the MongoClient on `global` -- same pattern as the mongoose cache in
// lib/db.ts. Without this, every Next.js dev-mode hot reload (and every cold
// serverless invocation once deployed) creates a brand new connection pool
// instead of reusing one, which is what was eating into Atlas's connection
// limit (353/500 seen in the dashboard before this fix).
declare global {
    var _authMongoClient: MongoClient | undefined;
}

const client = global._authMongoClient || new MongoClient(process.env.MONGODB_URI!);

if (!global._authMongoClient) {
    global._authMongoClient = client;
}

const db = client.db();

export const auth = betterAuth({
    database: mongodbAdapter(db, {
        client,
    }),
    emailAndPassword: {
        enabled: true
    },
});

export async function getSession(){
    const result = await auth.api.getSession({
        headers: await headers()
    });

    return result;
}

export async function signOut(){
    const result = await auth.api.signOut({
        headers: await headers()
    });
    
    if (result.success){
        redirect("/sign-in");
    }
}