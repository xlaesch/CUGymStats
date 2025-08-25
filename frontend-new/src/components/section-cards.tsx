import { IconTrendingDown, IconTrendingUp } from "@tabler/icons-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface SectionCardsProps {
  setSelectedGym: (gym: string) => void
}

export function SectionCards({ setSelectedGym }: SectionCardsProps) {
  const gymLocations = [
    {
      name: "Helen Newman Fitness Center",
      value: "helen-newman-fitness-center",
      capacity: "29%",
      trend: "up",
      lastCount: 23,
      status: "Busier than usual",
      gradient: "from-blue-50 to-blue-100",
    },
    {
      name: "HNH Court 1 Basketball",
      value: "hnh-court-1-basketball",
      capacity: "42%",
      trend: "down",
      lastCount: 18,
      status: "Less busy than usual",
      gradient: "from-blue-50 to-blue-100",
    },
    {
      name: "HNH Court 2 Volleyball/Badminton",
      value: "hnh-court-2-volleyball-badminton",
      capacity: "58%",
      trend: "down",
      lastCount: 24,
      status: "Less busy than usual",
      gradient: "from-orange-50 to-orange-100",
    },
    {
      name: "Noyes Court Basketball",
      value: "noyes-court-basketball",
      capacity: "12%",
      trend: "down",
      lastCount: 5,
      status: "Not busy",
      gradient: "from-blue-50 to-blue-100",
    },
    {
      name: "Noyes Fitness Center",
      value: "noyes-fitness-center",
      capacity: "65%",
      trend: "down",
      lastCount: 78,
      status: "Less busy than usual",
      gradient: "from-orange-50 to-orange-100",
    },
    {
      name: "Teagle Down Fitness Center",
      value: "teagle-down-fitness-center",
      capacity: "48%",
      trend: "down",
      lastCount: 52,
      status: "Less busy than usual",
      gradient: "from-blue-50 to-blue-100",
    },
    {
      name: "Teagle Up Fitness Center",
      value: "teagle-up-fitness-center",
      capacity: "83%",
      trend: "up",
      lastCount: 96,
      status: "Busier than usual",
      gradient: "from-orange-50 to-orange-100",
    },
    {
      name: "Toni Morrison Fitness Center",
      value: "toni-morrison-fitness-center",
      capacity: "92%",
      trend: "up",
      lastCount: 110,
      status: "As busy as it gets",
      gradient: "from-red-100 to-red-200",
      borderColor: "border-red-200",
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      {gymLocations.map((gym) => (
        <Card
          key={gym.value}
          className={`@container/card cursor-pointer bg-gradient-to-t ${gym.gradient} ${gym.borderColor || ""}`}
          onClick={() => setSelectedGym(gym.value)}
        >
          <CardHeader>
            <CardDescription>{gym.name}</CardDescription>
            <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
              {gym.capacity}
            </CardTitle>
            <CardAction>
              <Badge variant="outline">
                {gym.trend === "up" ? <IconTrendingUp /> : <IconTrendingDown />}
              </Badge>
            </CardAction>
          </CardHeader>
          <CardFooter className="flex-col items-start gap-1.5 text-sm">
            <div className="line-clamp-1 flex gap-2 font-medium">
              Last Count: {gym.lastCount}
            </div>
            <div className="text-muted-foreground">{gym.status}</div>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
