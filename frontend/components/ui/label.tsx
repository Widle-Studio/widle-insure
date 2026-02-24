import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
// import * as LabelPrimitive from "@radix-ui/react-label" // Assuming radix is installed, but if not, use simple label

// Since we cannot be sure if radix-ui is installed and working with npm issues, 
// I will create a standard HTML label that looks like the shadcn one.
// If radix is typically used, I'd use it, but safe bet is standard HTML for now given dependencies might be shaky.

const labelVariants = cva(
    "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
)

const Label = React.forwardRef<
    HTMLLabelElement,
    React.LabelHTMLAttributes<HTMLLabelElement> & VariantProps<typeof labelVariants>
>(({ className, ...props }, ref) => (
    <label
        ref={ref}
        className={cn(labelVariants(), className)}
        {...props}
    />
))
Label.displayName = "Label"

export { Label }
