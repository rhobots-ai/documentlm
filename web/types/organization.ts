export interface OrganizationConfiguration {
  theme: string
  logo_light: string
  logo_dark: string
  icon: string
  tagline: string
  is_white_labeled: string
  highlights: string[]
}

export interface AuthOrganization {
  id: string
  name: string
  slug: string
  createdAt: Date
  metadata?: any
  logo?: string | null | undefined
}

export interface Organization {
  id: string
  name: string
  slug: string
  members: number
  created: string
  metadata: OrganizationConfiguration
}