import Link from "next/link"

export default function AppLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <nav className="sticky top-0 z-40 w-full border-b bg-white px-4 py-3 shadow-sm">
          <div className="container mx-auto flex flex-col md:flex-row items-center justify-between gap-4 md:gap-0">
              <Link href="/dashboard" className="text-xl font-bold text-slate-900 tracking-tight">Widle Insure</Link>
              <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6">
                  <Link href="/dashboard" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">Dashboard</Link>
                  <Link href="/claims" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">Claims</Link>
                  <Link href="/settings" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">Settings</Link>
                  <Link href="/" className="text-sm font-medium text-slate-400 hover:text-slate-600 ml-4 border-l pl-4 border-slate-200 transition-colors">Logout</Link>
              </div>
          </div>
      </nav>
      <main className="container mx-auto py-8 flex-1 px-4">
          {children}
      </main>
    </div>
  )
}
