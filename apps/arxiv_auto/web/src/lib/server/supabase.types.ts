export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      baptaTours: {
        Row: {
          created_at: string
          email: string | null
          firstName: string | null
          id: number
          lastName: string | null
          message: string | null
          people: number | null
          tours: string | null
          whatsapp: string | null
        }
        Insert: {
          created_at?: string
          email?: string | null
          firstName?: string | null
          id?: number
          lastName?: string | null
          message?: string | null
          people?: number | null
          tours?: string | null
          whatsapp?: string | null
        }
        Update: {
          created_at?: string
          email?: string | null
          firstName?: string | null
          id?: number
          lastName?: string | null
          message?: string | null
          people?: number | null
          tours?: string | null
          whatsapp?: string | null
        }
        Relationships: []
      }
      "Contact Forms": {
        Row: {
          companyName: string | null
          created_at: string
          email: string | null
          id: number
          message: string | null
          name: string | null
          phone: string | null
          website: string | null
        }
        Insert: {
          companyName?: string | null
          created_at?: string
          email?: string | null
          id?: number
          message?: string | null
          name?: string | null
          phone?: string | null
          website?: string | null
        }
        Update: {
          companyName?: string | null
          created_at?: string
          email?: string | null
          id?: number
          message?: string | null
          name?: string | null
          phone?: string | null
          website?: string | null
        }
        Relationships: []
      }
      evaluated_submissions: {
        Row: {
          body: string
          correct_reason: string | null
          cost: number
          created_at: string
          human_answer: boolean | null
          id: string
          is_relevant: boolean
          qualifying_question: string | null
          reason: string | null
          reddit_id: string
          title: string
          url: string
        }
        Insert: {
          body?: string
          correct_reason?: string | null
          cost: number
          created_at?: string
          human_answer?: boolean | null
          id?: string
          is_relevant: boolean
          qualifying_question?: string | null
          reason?: string | null
          reddit_id: string
          title?: string
          url: string
        }
        Update: {
          body?: string
          correct_reason?: string | null
          cost?: number
          created_at?: string
          human_answer?: boolean | null
          id?: string
          is_relevant?: boolean
          qualifying_question?: string | null
          reason?: string | null
          reddit_id?: string
          title?: string
          url?: string
        }
        Relationships: []
      }
      leads: {
        Row: {
          comment: string | null
          data: Json | null
          discovered_at: string
          id: string
          last_contacted_at: string | null
          last_event: string
          prospect_name: string | null
          prospect_username: string
          reddit_id: string
          source: string
          status: string
          submission_id: string | null
        }
        Insert: {
          comment?: string | null
          data?: Json | null
          discovered_at?: string
          id?: string
          last_contacted_at?: string | null
          last_event?: string
          prospect_name?: string | null
          prospect_username: string
          reddit_id: string
          source?: string
          status: string
          submission_id?: string | null
        }
        Update: {
          comment?: string | null
          data?: Json | null
          discovered_at?: string
          id?: string
          last_contacted_at?: string | null
          last_event?: string
          prospect_name?: string | null
          prospect_username?: string
          reddit_id?: string
          source?: string
          status?: string
          submission_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "public_leads_submission_id_fkey"
            columns: ["submission_id"]
            isOneToOne: false
            referencedRelation: "evaluated_submissions"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type PublicSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (PublicSchema["Tables"] & PublicSchema["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (PublicSchema["Tables"] &
        PublicSchema["Views"])
    ? (PublicSchema["Tables"] &
        PublicSchema["Views"])[PublicTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof PublicSchema["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof PublicSchema["Enums"]
    ? PublicSchema["Enums"][PublicEnumNameOrOptions]
    : never
