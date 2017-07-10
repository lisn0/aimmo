from simulation.turn_manager import state_provider

class WorldState():
    """ A 'world state' is what the front-end sees. The front-end needs to
        know the players and a general world that is exposed at each moment in
        time.

        * get_update ---> an update is a modification of the world exposed
            via the socket connection
        * get_init ---> get the initial world state
    """

    def __init__(self):
        pass

    def get_update(self):
        pass

    def get_init(self):
        pass


class BrowserWorldState(WorldState):
    def __init__(self, game_state):
        super().__init__()
        self.game_state = game_state

    # Note the browser does both the update and the init the same.
    # In an ideal case, we should not retransmit static objects such as obstacles at each call.
    def get_update(self):
        return self.__get_world_state()
    def get_init(self):
        return self.__get_world_state()

    def __get_world_state(self):
        # Cells are given a code(0, 1, 2) for the brower display
        def to_cell_type(cell):
            if not cell.habitable:
                return 1
            if cell.generates_score:
                return 2
            return 0

        # Players have also some visual charachteristics
        def player_dict(avatar):
            # TODO: implement better colour functionality: will eventually fall off end of numbers
            colour = "#%06x" % (avatar.player_id * 4999)
            return {
                'id': avatar.player_id,
                'x': avatar.location.x,
                'y': avatar.location.y,
                'health': avatar.health,
                'score': avatar.score,
                'rotation': 0,
                "colours": {
                    "bodyStroke": "#0ff",
                    "bodyFill": colour,
                    "eyeStroke": "#aff",
                    "eyeFill": "#eff",
                }
            }

        with self.game_state as game_state:
            world = game_state.world_map
            player_data = {p.player_id: player_dict(p) for p in game_state.avatar_manager.avatars}
            grid_dict = defaultdict(dict)
            for cell in world.all_cells():
                grid_dict[cell.location.x][cell.location.y] = to_cell_type(cell)
            pickups = []
            for cell in world.pickup_cells():
                pickup = cell.pickup.serialise()
                pickup['location'] = (cell.location.x, cell.location.y)
                pickups.append(pickup)
            return {
                    'players': player_data,
                    'score_locations': [(cell.location.x, cell.location.y) for cell in world.score_cells()],
                    'pickups': pickups,
                    # TODO: experiment with only sending deltas (not if not required)
                    'map_changed': True,
                    'width': world.num_cols,
                    'height': world.num_rows,
                    'minX': world.min_x(),
                    'minY': world.min_y(),
                    'maxX': world.max_x(),
                    'maxY': world.max_y(),
                    'layout': grid_dict,
                }
