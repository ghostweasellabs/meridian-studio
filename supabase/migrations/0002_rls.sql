-- Enable RLS
ALTER TABLE graphs ENABLE ROW LEVEL SECURITY;
ALTER TABLE graph_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_graphs ENABLE ROW LEVEL SECURITY;

-- Only owners can select/modify own graphs
CREATE POLICY "Users can view own graphs" ON graphs
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can modify own graphs" ON graphs
  FOR ALL USING (auth.uid() = user_id);

-- Users can view graphs shared with them or public
CREATE POLICY "Users can view shared graphs" ON graphs
  FOR SELECT USING (
    is_public = TRUE OR id IN (
      SELECT graph_id FROM shared_graphs
      WHERE shared_with = auth.uid() OR shared_with IS NULL
    )
  );

-- Graph executions: only owner can view
CREATE POLICY "Users can view own executions" ON graph_executions
  FOR SELECT USING (auth.uid() = user_id);

-- Shared graphs table: owner can manage entries
CREATE POLICY "Owners manage shared graphs" ON shared_graphs
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM graphs g WHERE g.id = shared_graphs.graph_id AND g.user_id = auth.uid()
    )
  );
