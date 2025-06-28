import {Beaker, BellDot, BookOpen, Brain, FlaskRound as Flask, Microscope, Users} from 'lucide-vue-next'

const iconMap = {
  Brain,
  Microscope,
  Book: BookOpen,
  Users,
  Beaker,
  Flask,
  BellDot
} as const

export function getSpaceIconComponent(icon: string) {
  return iconMap[icon as keyof typeof iconMap] || BookOpen
}
