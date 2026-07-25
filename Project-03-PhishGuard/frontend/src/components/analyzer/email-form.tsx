import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Loader2, ScanSearch } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input, Textarea } from "@/components/ui/input"

const emailSchema = z.object({
  sender: z.string().max(255).optional().or(z.literal("")),
  subject: z.string().max(500).optional().or(z.literal("")),
  raw_content: z.string().min(1, "Paste the email content to analyze."),
})

export type EmailFormValues = z.infer<typeof emailSchema>

interface EmailFormProps {
  onSubmit: (values: EmailFormValues) => void
  submitting: boolean
}

const SAMPLE_EMAIL = `From: security-alert@micros0ft-support.com
Subject: Urgent: Verify your account now

Dear user,

Your Microsoft account will be suspended within 24 hours due to unusual sign-in activity.
Act now and confirm your password immediately at http://192.168.10.5/verify to avoid suspension.

Microsoft Account Team`

export function EmailForm({ onSubmit, submitting }: EmailFormProps) {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<EmailFormValues>({
    resolver: zodResolver(emailSchema),
    defaultValues: { sender: "", subject: "", raw_content: "" },
  })

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col gap-4 rounded-xl border border-border bg-card p-5"
    >
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1.5 block text-xs font-medium text-muted-foreground">
            Sender (optional)
          </label>
          <Input placeholder="alerts@example.com" {...register("sender")} />
        </div>
        <div>
          <label className="mb-1.5 block text-xs font-medium text-muted-foreground">
            Subject (optional)
          </label>
          <Input placeholder="Account verification required" {...register("subject")} />
        </div>
      </div>

      <div>
        <div className="mb-1.5 flex items-center justify-between">
          <label className="block text-xs font-medium text-muted-foreground">
            Raw Email Content
          </label>
          <button
            type="button"
            onClick={() => setValue("raw_content", SAMPLE_EMAIL, { shouldValidate: true })}
            className="cursor-pointer text-xs font-medium text-primary hover:underline"
          >
            Load sample phishing email
          </button>
        </div>
        <Textarea
          rows={12}
          placeholder="Paste the full email, including headers if available..."
          {...register("raw_content")}
        />
        {errors.raw_content && (
          <p className="mt-1 text-xs text-critical">{errors.raw_content.message}</p>
        )}
      </div>

      <Button type="submit" disabled={submitting} className="gap-2 self-start">
        {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <ScanSearch className="h-4 w-4" />}
        {submitting ? "Analyzing..." : "Analyze Email"}
      </Button>
    </form>
  )
}
