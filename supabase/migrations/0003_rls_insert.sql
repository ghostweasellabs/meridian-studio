-- Allow owners to insert graphs
CREATE POLICY "Users can insert own graphs" ON graphs
  FOR INSERT WITH CHECK (auth.uid() = user_id);
