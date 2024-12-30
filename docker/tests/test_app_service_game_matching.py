import unittest
from src.app.services.validation.bot_game_validator import GameMatchingValidator


class TestGameMatchingValidator(unittest.TestCase):
    # @patch("src.app.utils.class_retriever.ClassRetriever")
    # @patch("src.app.services.file_loader.file_loader.FileLoader")
    def test_validate_successful(self):
        bot_path = "docker/tests/sample_bots/game_match/correct_bot.py"
        game_path = "docker/src/two_player_games/games/morris.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        result = validator.validate()

        # Assertions
        self.assertEqual(result, True)

    def test_no_bot_class_found(self):
        bot_path = "docker/tests/sample_bots/game_match/no_inheritance.py"
        game_path = "docker/src/two_player_games/games/connect_four.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(str(context.exception), "No class inheriting from Bot found.")

    def test_no_bot_class_syntax_error(self):
        bot_path = "docker/tests/sample_bots/game_match/syntax_error.py"
        game_path = "docker/src/two_player_games/games/connect_four.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(SyntaxError) as context:
            validator.validate()

        # Assertions

    def test_no_bot_class_found_only_method(self):
        bot_path = "docker/tests/sample_bots/game_match/no_class.py"
        game_path = "docker/src/two_player_games/games/connect_four.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(str(context.exception), "No class inheriting from Bot found.")

    def test_no_bot_class_found_empty(self):
        bot_path = "docker/tests/sample_bots/game_match/empty.py"
        game_path = "docker/src/two_player_games/games/connect_four.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(str(context.exception), "No class inheriting from Bot found.")

    def test_multiple_bot_classes_found(self):
        bot_path = "docker/tests/sample_bots/game_match/multiple_inheritance.py"
        game_path = "docker/src/two_player_games/games/dots_and_boxes.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(
            str(context.exception),
            "Multiple classes inherit from Bot. Only one is allowed.",
        )

    def test_invalid_get_move_signature_too_many_args(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_get_move.py"
        game_path = "docker/src/two_player_games/games/nim.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "'get_move' method in Bot_1 must accept exactly one argument 'state'.",
            str(context.exception),
        )

    def test_invalid_get_move_signature_wrong_arg_name(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_get_move_name.py"
        game_path = "docker/src/two_player_games/games/nim.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "'get_move' method in Bot_1 must accept exactly one argument 'state'.",
            str(context.exception),
        )

    def test_invalid_get_move_signature_no_get_move(self):
        bot_path = "docker/tests/sample_bots/game_match/no_get_move.py"
        game_path = "docker/src/two_player_games/games/nim.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Class Bot_1 does not implement 'get_move' method.",
            str(context.exception),
        )

    def test_invalid_get_move_signature_wrong_arg_self(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_get_move_name_self.py"
        game_path = "docker/src/two_player_games/games/nim.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()
        # Assertions
        self.assertIn(
            "'get_move' method in Bot_1 must accept exactly one argument 'state'.",
            str(context.exception),
        )

    def test_invalid_move_return_type(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_move_type.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_move_return_type_int(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_move_type_int.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_move_return_type_none(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_move_type_none.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameMatchingValidator(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
