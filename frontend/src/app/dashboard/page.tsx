"use client"

import * as React from "react"
import { ChartAreaInteractive } from "@/components/chart-area-interactive"
import { SectionCards } from "@/components/section-cards"
import { SiteHeader } from "@/components/site-header"

export default function Page() {
  const [selectedGym, setSelectedGym] = React.useState(
    "helen-newman-fitness-center"
  )

  return (
    <div
      style={
        {
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties
      }
      className="flex min-h-svh w-full flex-col"
    >
      <SiteHeader showSidebarTrigger={false} />
      <div className="flex flex-1 flex-col">
        <div className="@container/main flex flex-1 flex-col gap-2">
          <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
            <SectionCards setSelectedGym={setSelectedGym} />
            <div className="px-4 lg:px-6">
              <ChartAreaInteractive
                selectedGym={selectedGym}
                setSelectedGym={setSelectedGym}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
