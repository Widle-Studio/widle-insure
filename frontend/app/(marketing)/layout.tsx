import Link from "next/link"

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <header className="sticky top-0 z-40 w-full border-b bg-white shadow-sm">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-xl font-bold text-slate-900 tracking-tight">Widle Insure</span>
            </Link>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="#features" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
              Features
            </Link>
            <Link href="#how-it-works" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
              How it Works
            </Link>
            <Link href="/login" className="text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md transition-colors">
              Login / Get Started
            </Link>
          </nav>
          <div className="md:hidden">
             <Link href="/login" className="text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md transition-colors">
              Login
            </Link>
          </div>
        </div>
      </header>
      <main className="flex-1">{children}</main>
      <footer className="border-t bg-slate-900 py-12 text-slate-400">
        <div className="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
                <span className="text-xl font-bold text-white tracking-tight mb-4 block">Widle Insure</span>
                <p className="text-sm">AI-Automated Auto Insurance Claims Platform.</p>
            </div>
            <div>
                <h3 className="text-white font-medium mb-4">Product</h3>
                <ul className="space-y-2 text-sm">
                    <li><Link href="#features" className="hover:text-white transition-colors">Features</Link></li>
                    <li><Link href="#how-it-works" className="hover:text-white transition-colors">How it Works</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Pricing</Link></li>
                </ul>
            </div>
             <div>
                <h3 className="text-white font-medium mb-4">Company</h3>
                <ul className="space-y-2 text-sm">
                    <li><Link href="#" className="hover:text-white transition-colors">About</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Careers</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Contact</Link></li>
                </ul>
            </div>
             <div>
                <h3 className="text-white font-medium mb-4">Legal</h3>
                <ul className="space-y-2 text-sm">
                    <li><Link href="#" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Terms of Service</Link></li>
                </ul>
            </div>
        </div>
        <div className="container mx-auto px-4 mt-12 pt-8 border-t border-slate-800 text-sm text-center">
            &copy; {new Date().getFullYear()} Widle Insure. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
