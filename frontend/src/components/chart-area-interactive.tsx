"use client"

import * as React from "react"
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@/components/ui/toggle-group"

export const description = "An interactive area chart"

type AvgPoint = { hour: number; avg_percentage: number | null }
type ChartPoint = { time: string; visitors: number }

function toTimeLabel(hour: number): string {
  const h = ((hour % 24) + 24) % 24
  const ampm = h >= 12 ? "pm" : "am"
  const display = h % 12 === 0 ? 12 : h % 12
  return `${display}${ampm}`
}

const chartConfig = {
  visitors: {
    label: "Visitors",
    color: "var(--primary)",
  },
} satisfies ChartConfig

interface ChartAreaInteractiveProps {
  selectedGym: string
  setSelectedGym: (gym: string) => void
}

export function ChartAreaInteractive({
  selectedGym,
  setSelectedGym,
}: ChartAreaInteractiveProps) {
  const [timeRange, setTimeRange] = React.useState("90d")
  const [selectedDay, setSelectedDay] = React.useState("monday")
  const [data, setData] = React.useState<ChartPoint[]>([])
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const dayMap: Record<string, number> = {
    monday: 0,
    tuesday: 1,
    wednesday: 2,
    thursday: 3,
    friday: 4,
    saturday: 5,
    sunday: 6,
  }

  // Define gym options before any memo/effect that depends on them
  const gymOptions = [
    {
      value: "helen-newman-fitness-center",
      label: "Helen Newman Fitness Center",
    },
    { value: "hnh-court-1-basketball", label: "HNH Court 1 Basketball" },
    {
      value: "hnh-court-2-volleyball-badminton",
      label: "HNH Court 2 Volleyball/Badminton",
    },
    { value: "noyes-court-basketball", label: "Noyes Court Basketball" },
    { value: "noyes-fitness-center", label: "Noyes Fitness Center" },
    {
      value: "teagle-down-fitness-center",
      label: "Teagle Down Fitness Center",
    },
    { value: "teagle-up-fitness-center", label: "Teagle Up Fitness Center" },
    {
      value: "toni-morrison-fitness-center",
      label: "Toni Morrison Fitness Center",
    },
  ]

  const defaultLocation = "Helen Newman Fitness Center"
  const slugToLabel = React.useMemo(() => {
    const m = new Map<string, string>()
    for (const g of gymOptions) m.set(g.value, g.label)
    return m
  }, [])

  React.useEffect(() => {
    const dayIdx = dayMap[selectedDay] ?? 0
    setLoading(true)
    setError(null)
    // Resolve table name from current selection; fall back to a safe default
    const location = slugToLabel.get(selectedGym) || defaultLocation
    // Calls the Next.js BFF route
    fetch(`/api/average-occupancy?dayofweek=${dayIdx}&location=${encodeURIComponent(location)}`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`Request failed ${r.status}`)
        const json = (await r.json()) as AvgPoint[]
        const points: ChartPoint[] = json.map((p) => ({
          time: toTimeLabel(p.hour),
          visitors: Math.max(0, Math.round((p.avg_percentage ?? 0))),
        }))
        setData(points)
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [selectedDay, selectedGym, slugToLabel])

  // gymOptions defined above

  const dayOptions = [
    { value: "monday", label: "Monday" },
    { value: "tuesday", label: "Tuesday" },
    { value: "wednesday", label: "Wednesday" },
    { value: "thursday", label: "Thursday" },
    { value: "friday", label: "Friday" },
    { value: "saturday", label: "Saturday" },
    { value: "sunday", label: "Sunday" },
  ]

  const selectedDayLabel = dayOptions.find(
    (day) => day.value === selectedDay
  )?.label
  const selectedGymLabel = gymOptions.find(
    (gym) => gym.value === selectedGym
  )?.label

  return (
    <Card className="@container/card transition-none hover:shadow-none hover:translate-y-0 hover:-translate-y-0 hover:border-border">
      <CardHeader>
        <div className="flex flex-wrap items-center gap-2">
          <CardTitle>Historical Gym Data for</CardTitle>
          <Select value={selectedDay} onValueChange={setSelectedDay}>
            <SelectTrigger className="w-auto" aria-label="Select a day">
              <SelectValue placeholder="Select a day" />
            </SelectTrigger>
            <SelectContent className="rounded-xl">
              {dayOptions.map((day) => (
                <SelectItem
                  key={day.value}
                  value={day.value}
                  className="rounded-lg"
                >
                  {day.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <CardTitle>at</CardTitle>
          <Select value={selectedGym} onValueChange={setSelectedGym}>
            <SelectTrigger className="w-auto" aria-label="Select a gym">
              <SelectValue placeholder="Select a gym" />
            </SelectTrigger>
            <SelectContent className="rounded-xl">
              {gymOptions.map((gym) => (
                <SelectItem
                  key={gym.value}
                  value={gym.value}
                  className="rounded-lg"
                >
                  {gym.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <CardAction>
          <ToggleGroup
            type="single"
            value={timeRange}
            onValueChange={setTimeRange}
            variant="outline"
            className="hidden *:data-[slot=toggle-group-item]:!px-4 @[767px]/card:flex"
          >
            <ToggleGroupItem value="90d">Last 3 months</ToggleGroupItem>
            <ToggleGroupItem value="30d">Last 30 days</ToggleGroupItem>
            <ToggleGroupItem value="7d">Last 7 days</ToggleGroupItem>
          </ToggleGroup>
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger
              className="flex w-40 **:data-[slot=select-value]:block **:data-[slot=select-value]:truncate @[767px]/card:hidden"
              size="sm"
              aria-label="Select a value"
            >
              <SelectValue placeholder="Last 3 months" />
            </SelectTrigger>
            <SelectContent className="rounded-xl">
              <SelectItem value="90d" className="rounded-lg">
                Last 3 months
              </SelectItem>
              <SelectItem value="30d" className="rounded-lg">
                Last 30 days
              </SelectItem>
              <SelectItem value="7d" className="rounded-lg">
                Last 7 days
              </SelectItem>
            </SelectContent>
          </Select>
        </CardAction>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        {error && (
          <div className="text-sm text-destructive mb-2">{error}</div>
        )}
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <AreaChart data={data} margin={{ left: 12, right: 20 }}>
            <defs>
              <linearGradient id="fillVisitors" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-visitors)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-visitors)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="time"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              interval={0}
              tickFormatter={(value) => value}
            />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={(value) => value}
                  indicator="dot"
                />
              }
            />
            <Area
              dataKey="visitors"
              type="natural"
              fill="url(#fillVisitors)"
              stroke="var(--color-visitors)"
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
