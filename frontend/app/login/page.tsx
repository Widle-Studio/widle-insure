"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { apiClient } from "@/lib/api-client";
import { Shield, Loader2 } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'error'>('checking');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check backend connection on mount
    apiClient.get("/health")
      .then(res => {
        if (res.data.status === 'healthy') {
            setBackendStatus('connected');
        } else {
            setBackendStatus('error');
        }
      })
      .catch(() => setBackendStatus('error'));
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    // Simulate authentication delay
    setTimeout(() => {
        if (backendStatus !== 'connected') {
            setError("Cannot connect to backend server. Please try again later.");
            setIsLoading(false);
            return;
        }

        // On successful "login", redirect to the dashboard
        router.push("/dashboard");
    }, 1000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-md">
        <div className="flex justify-center mb-8">
            <div className="flex items-center space-x-2">
                <Shield className="w-8 h-8 text-blue-600" />
                <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Widle Insure</h1>
            </div>
        </div>

        <Card className="border-slate-200 shadow-md">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center">Sign in</CardTitle>
            <CardDescription className="text-center">
              Enter your admin credentials to access the portal
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleLogin}>
            <CardContent className="space-y-4">
              {error && (
                  <div className="p-3 bg-red-50 text-red-600 text-sm rounded-md border border-red-200">
                      {error}
                  </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="admin@widle.insure"
                  required
                  defaultValue="admin@widle.insure"
                  className="bg-white"
                />
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Password</Label>
                  <a href="#" className="text-xs text-blue-600 hover:text-blue-800 font-medium">Forgot password?</a>
                </div>
                <Input
                  id="password"
                  type="password"
                  required
                  defaultValue="password"
                  className="bg-white"
                />
              </div>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={isLoading || backendStatus === 'checking'}>
                {isLoading ? (
                    <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Signing in...
                    </>
                ) : (
                    "Sign in"
                )}
              </Button>

              {/* Status Indicator */}
              <div className="flex items-center justify-center space-x-2 text-xs">
                  {backendStatus === 'checking' && (
                      <span className="text-slate-500 flex items-center"><Loader2 className="mr-1 h-3 w-3 animate-spin" /> Checking backend connection...</span>
                  )}
                  {backendStatus === 'connected' && (
                      <span className="text-green-600 flex items-center">
                          <span className="inline-block h-2 w-2 rounded-full bg-green-500 mr-2"></span>
                          Backend connected
                      </span>
                  )}
                  {backendStatus === 'error' && (
                      <span className="text-red-500 flex items-center">
                          <span className="inline-block h-2 w-2 rounded-full bg-red-500 mr-2"></span>
                          Backend disconnected
                      </span>
                  )}
              </div>
            </CardFooter>
          </form>
        </Card>

        <p className="text-center text-sm text-slate-500 mt-8">
            &copy; {new Date().getFullYear()} Widle Insure. All rights reserved.
        </p>
      </div>
    </div>
  );
}
