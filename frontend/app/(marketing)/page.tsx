import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, CheckCircle2, Shield, Zap, Clock, Banknote } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="bg-slate-50 py-20 lg:py-32 border-b">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl lg:text-6xl font-extrabold text-slate-900 tracking-tight mb-6 max-w-4xl mx-auto">
            The Future of Auto Insurance Claims is <span className="text-blue-600">AI-Automated</span>
          </h1>
          <p className="text-lg lg:text-xl text-slate-600 mb-10 max-w-2xl mx-auto">
            Widle Insure accelerates your claim workflow from FNOL to payout. Experience end-to-end automation with deterministic guardrails.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/login">
              <Button size="lg" className="h-12 px-8 text-base bg-blue-600 hover:bg-blue-700">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link href="#features">
              <Button size="lg" variant="outline" className="h-12 px-8 text-base bg-white">
                Learn More
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Powerful Features</h2>
            <p className="text-slate-600 max-w-2xl mx-auto">Our platform combines cutting-edge AI with strict deterministic rules to handle claims efficiently and securely.</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
             <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <Clock className="w-10 h-10 text-blue-600 mb-2" />
                <CardTitle>End-to-End FNOL</CardTitle>
                <CardDescription>Intake in under 5 minutes</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 text-sm">
                  Streamlined mobile-first web forms for quick incident reporting, including multi-photo uploads and context gathering.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <Zap className="w-10 h-10 text-blue-600 mb-2" />
                <CardTitle>AI Damage Assessment</CardTitle>
                <CardDescription>Vision-based analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 text-sm">
                  Powered by advanced AI vision, accurately detect damage severity, affected parts, and estimate repair costs instantly.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <Shield className="w-10 h-10 text-blue-600 mb-2" />
                <CardTitle>Auto-Adjudication</CardTitle>
                <CardDescription>Strict deterministic guardrails</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 text-sm">
                  Safely auto-approve simple claims using hard limits, fraud scoring, and coverage checks, routing complex cases to humans.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <Banknote className="w-10 h-10 text-blue-600 mb-2" />
                <CardTitle>Instant Payouts</CardTitle>
                <CardDescription>Seamless integrations</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 text-sm">
                  Once approved, initiate secure payouts directly to claimant accounts with automated confirmation tracking.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section id="how-it-works" className="py-20 bg-slate-50 border-t">
        <div className="container mx-auto px-4">
           <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">How it Works</h2>
            <p className="text-slate-600 max-w-2xl mx-auto">From incident to resolution in three simple steps.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative">
            <div className="hidden md:block absolute top-12 left-1/6 right-1/6 h-0.5 bg-blue-100 z-0"></div>

            <div className="relative z-10 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center text-xl font-bold mb-6 border-4 border-slate-50">1</div>
              <h3 className="text-xl font-semibold text-slate-900 mb-2">Submit Claim</h3>
              <p className="text-slate-600">Claimant fills out an intuitive FNOL form and uploads photos of the damage from any device.</p>
            </div>

            <div className="relative z-10 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center text-xl font-bold mb-6 border-4 border-slate-50">2</div>
              <h3 className="text-xl font-semibold text-slate-900 mb-2">AI Analysis</h3>
              <p className="text-slate-600">Our engine assesses damage, cross-references policies, and checks fraud indicators in seconds.</p>
            </div>

            <div className="relative z-10 flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center text-xl font-bold mb-6 border-4 border-slate-50">3</div>
              <h3 className="text-xl font-semibold text-slate-900 mb-2">Review & Payout</h3>
              <p className="text-slate-600">Simple claims are auto-approved for instant payout, while complex ones are flagged for expert review.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">Ready to transform your claims process?</h2>
          <p className="text-blue-100 mb-10 max-w-2xl mx-auto text-lg">
            Join the platform that is redefining efficiency and accuracy in auto insurance.
          </p>
          <Link href="/login">
            <Button size="lg" variant="secondary" className="h-12 px-8 text-base text-blue-600 bg-white hover:bg-slate-100">
              Start Managing Claims
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
