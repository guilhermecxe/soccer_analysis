import pandas as pd

TABLE_COLS = ['Times', 'Pontos', 'Jogos', 'Vitórias', 'Empates', 'Derrotas', 'GP', 'GC', 'SG']
MATCHES_COLS = ['date', 'gameweek', 'home', 'home_score', 'away_score', 'away']

class Championship():
    def __init__(self, teams):
        def setup_table(teams):
            table = pd.DataFrame(columns=TABLE_COLS)
            table['Times'] = teams
            table.index += 1
            return table.fillna(0)
        def setup_matches():
            return pd.DataFrame(columns=MATCHES_COLS)

        self.table = setup_table(teams)
        self.matches = setup_matches()
        self.positions = dict.fromkeys(teams)
        for key in self.positions: self.positions[key] = []

    def add_matches(self, new_matches):
        self.matches = pd.concat([self.matches, new_matches])

        for _, row in new_matches.iterrows():
            self.update_table(row.home, row.home_score, row.away_score)
            self.update_table(row.away, row.away_score, row.home_score)
            self.positions[row.home].append([int(self.get_position(row.home)), row['date']])
            self.positions[row.away].append([int(self.get_position(row.away)), row['date']])
            # A posição de um time é atualizada sempre que ele joga, por isso, às vezes, dois times podem ter a mesma posição numa mesma data

    def update_table(self, team, goals, goals_against):
        for col in ['Jogos', 'GP', 'GC', 'SG']:
            if col == 'Jogos': value = 1
            if col == 'GP': value = goals
            if col == 'GC': value = goals_against
            if col == 'SG': value = goals - goals_against

            self.table.loc[self.table['Times'] == team, col] += value
        
        if goals == goals_against:
            self.table.loc[self.table['Times'] == team, 'Pontos'] += 1
            self.table.loc[self.table['Times'] == team, 'Empates'] += 1
        elif goals > goals_against:
            self.table.loc[self.table['Times'] == team, 'Pontos'] += 3
            self.table.loc[self.table['Times'] == team, 'Vitórias'] += 1
        elif goals_against > goals:
            self.table.loc[self.table['Times'] == team, 'Derrotas'] += 1

        self.table.sort_values(['Pontos', 'Vitórias', 'Derrotas', 'SG', 'GP', 'GC'], ascending=[0, 0, 1, 0, 0, 1], inplace=True)
        self.table.reset_index(drop=True, inplace=True)
        self.table.index += 1

    def __repr__(self):
        return str(self.table)

    def get_position(self, team):
        return self.table.index[self.table['Times'] == team][0]

    def get_positions_over_time(self, team):
        for team_ in self.table['Times']: # Atualizando a última posição de cada time para que dois ou mais não ocupem a mesma posição
            self.positions[team_][-1][0] = self.get_position(team_)
        return self.positions[team]