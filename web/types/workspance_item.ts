export interface WorkspaceItem {
  id: string
  name: string
  path?: string
  expanded?: boolean
  isEditing?: boolean
  editName?: string
  items?: WorkspaceItem[]
  parentId?: string
}