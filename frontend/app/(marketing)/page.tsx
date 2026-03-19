import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { CheckCircle2, Zap, ShieldCheck, Banknote } from "lucide-react";

export default function MarketingPage() {
    return (
        <div className="flex flex-col min-h-screen">
            <section className="space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-32">
                <div className="container flex max-w-[64rem] flex-col items-center gap-4 text-center">
                    <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight">
                        Revolutionizing Auto Insurance Claims with AI
                    </h1>
                    <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
                        Experience the future of First Notice of Loss. Automated damage assessment, instant adjudication, and faster payouts.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 mt-6 w-full px-4 sm:w-auto sm:px-0">
                        <Button size="lg" className="shadow-material-2 w-full sm:w-auto" asChild>
                            <a href="/login">Get Started</a>
                        </Button>
                        <Button variant="outline" size="lg" className="shadow-material-1 w-full sm:w-auto">
                            Learn More
                        </Button>
                    </div>
                </div>
            </section>

            <section className="container space-y-6 py-8 md:py-12 lg:py-24">
                <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
                    <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl font-bold">Key Features</h2>
                    <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
                        Our platform dramatically reduces processing time and increases accuracy.
                    </p>
                </div>

                <div className="mx-auto grid justify-center gap-4 grid-cols-1 sm:grid-cols-2 md:max-w-[64rem] md:grid-cols-2 lg:grid-cols-4 mt-8 px-4">
                    <Card className="shadow-material-2 hover:shadow-material-4 transition-shadow">
                        <CardHeader>
                            <Zap className="h-10 w-10 mb-4 text-primary" />
                            <CardTitle>End-to-End FNOL</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <CardDescription>Streamlined digital intake process for a seamless customer experience.</CardDescription>
                        </CardContent>
                    </Card>

                    <Card className="shadow-material-2 hover:shadow-material-4 transition-shadow">
                        <CardHeader>
                            <CheckCircle2 className="h-10 w-10 mb-4 text-primary" />
                            <CardTitle>AI Damage Assessment</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <CardDescription>Advanced computer vision accurately evaluates damage from photos in seconds.</CardDescription>
                        </CardContent>
                    </Card>

                    <Card className="shadow-material-2 hover:shadow-material-4 transition-shadow">
                        <CardHeader>
                            <ShieldCheck className="h-10 w-10 mb-4 text-primary" />
                            <CardTitle>Auto-Adjudication</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <CardDescription>Intelligent rules engine determines coverage and limits without human intervention.</CardDescription>
                        </CardContent>
                    </Card>

                    <Card className="shadow-material-2 hover:shadow-material-4 transition-shadow">
                        <CardHeader>
                            <Banknote className="h-10 w-10 mb-4 text-primary" />
                            <CardTitle>Instant Payouts</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <CardDescription>Approved claims are settled and paid out instantly to the policyholder.</CardDescription>
                        </CardContent>
                    </Card>
                </div>
            </section>
        </div>
    );
}
