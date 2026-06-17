import { Save } from 'lucide-react'
import { AppShell } from '@/components/app-shell'
import { PageHeader, Button } from '@/components/ui'
import { FaturaForm } from '@/components/fatura-form'

export default function FaturaPage() {
  return (
    <AppShell>
      <PageHeader
        title="Fatura Girişi"
        subtitle="Fatura, satın alma ve irsaliye karşılaştırma modeli"
        actions={
          <Button>
            <Save className="size-4" />
            Faturayı Kaydet
          </Button>
        }
      />
      <div className="mt-6">
        <FaturaForm />
      </div>
    </AppShell>
  )
}
