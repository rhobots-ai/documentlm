import type {Space} from "~/types/space";

export interface UpdateTagRequest {
  name?: string,
  color?: string,
  parent_id?: string
  spaces_to_tag?: string[]
  spaces_to_untag?: string[]
}

export interface Tag {
  id: string
  name: string
  color: string
  organization_id?: string
  parent_id?: string
  parent: Tag
  spaces: Space[]
}