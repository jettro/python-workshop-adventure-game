import { useState, useRef, useEffect, useCallback } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  Grid,
  Heading,
  HStack,
  Icon,
  Text,
  VStack,
  Badge,
} from "@chakra-ui/react";
import {
  LuTreePine,
  LuSkull,
  LuGamepad2,
  LuHouse,
  LuMapPin,
  LuCompass,
  LuArrowUp,
  LuArrowDown,
  LuArrowLeft,
  LuArrowRight,
  LuPlay,
  LuSquare,
  LuSword,
} from "react-icons/lu";
import { startGame, movePlayer, stopGame } from "./api";
import VictoryScreen from "./VictoryScreen";

const COMPASS_MAP = {
  NORTH: { icon: LuArrowUp, label: "North" },
  NORTH_EAST: { icon: LuArrowUp, label: "North East" },
  EAST: { icon: LuArrowRight, label: "East" },
  SOUTH_EAST: { icon: LuArrowDown, label: "South East" },
  SOUTH: { icon: LuArrowDown, label: "South" },
  SOUTH_WEST: { icon: LuArrowDown, label: "South West" },
  WEST: { icon: LuArrowLeft, label: "West" },
  NORTH_WEST: { icon: LuArrowUp, label: "North West" },
  HERE: { icon: LuMapPin, label: "You are at the Exit!" },
};

function MaterialIcon({ name, ...props }) {
  return (
    <span className="material-icons" {...props}>
      {name}
    </span>
  );
}

export default function App() {
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const logEndRef = useRef(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [game?.messages]);

  const handleStart = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const state = await startGame();
      setGame(state);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleMove = useCallback(
    async (direction) => {
      if (!game || game.finished || loading) return;
      setLoading(true);
      setError(null);
      try {
        const state = await movePlayer(game.game_id, direction);
        setGame(state);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    },
    [game, loading]
  );

  const handleStop = useCallback(async () => {
    if (!game || game.finished) return;
    setLoading(true);
    try {
      await stopGame(game.game_id);
      setGame((prev) => ({ ...prev, finished: true, messages: [...prev.messages, "Game stopped by user."] }));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [game]);

  // Keyboard controls
  useEffect(() => {
    const handleKey = (e) => {
      const map = { ArrowUp: "N", ArrowDown: "S", ArrowLeft: "W", ArrowRight: "E" };
      if (map[e.key]) {
        e.preventDefault();
        handleMove(map[e.key]);
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [handleMove]);

  const compass = game?.compass ? COMPASS_MAP[game.compass] : null;
  const isVictory = game?.finished && game?.compass === "HERE";

  // Victory — show victory screen
  if (isVictory) {
    return (
      <VictoryScreen
        game={game}
        onPlayAgain={handleStart}
        onReturnToMenu={() => setGame(null)}
      />
    );
  }

  // No game started — show splash
  if (!game) {
    return (
      <Flex minH="100vh" align="center" justify="center" direction="column" gap={6}>
        <HStack gap={3}>
          <Icon fontSize="3xl" color="#f4c025">
            <LuSword />
          </Icon>
          <Heading size="2xl" fontWeight="bold" color="#f4c025">
            Adventure Realm
          </Heading>
        </HStack>
        <Text color="gray.400" fontSize="lg">
          Navigate the board, find the exit, and maximise your score.
        </Text>
        <Button
          size="lg"
          bg="#f4c025"
          color="black"
          _hover={{ bg: "#d4a520" }}
          onClick={handleStart}
          loading={loading}
        >
          <LuPlay /> New Game
        </Button>
        {error && (
          <Text color="red.400" fontSize="sm">
            {error}
          </Text>
        )}
      </Flex>
    );
  }

  return (
    <Container maxW="1200px" py={6}>
      {/* Header */}
      <Flex align="center" justify="space-between" mb={6}>
        <HStack gap={3}>
          <Icon fontSize="2xl" color="#f4c025">
            <LuSword />
          </Icon>
          <Heading size="xl" fontWeight="bold" color="#f4c025">
            Adventure Realm
          </Heading>
          <Text color="gray.500" fontSize="sm">
            — Game Board
          </Text>
        </HStack>
        <HStack gap={3}>
          {!game.finished && (
            <Button size="sm" variant="outline" colorPalette="red" onClick={handleStop} disabled={loading}>
              <LuSquare /> Stop
            </Button>
          )}
          <Button size="sm" bg="#f4c025" color="black" _hover={{ bg: "#d4a520" }} onClick={handleStart} disabled={loading}>
            <LuPlay /> New Game
          </Button>
        </HStack>
      </Flex>

      <Grid templateColumns={{ base: "1fr", md: "300px 1fr" }} gap={6}>
        {/* Left sidebar — Status */}
        <VStack gap={4} align="stretch">
          {/* Score card */}
          <Box bg="#1a1d27" borderRadius="xl" p={5} borderWidth="1px" borderColor="#2d3148">
            <Text fontSize="xs" color="gray.500" fontWeight="600" textTransform="uppercase" mb={1}>
              Score
            </Text>
            <Heading size="3xl" color="#f4c025" fontWeight="bold">
              {game.score}
            </Heading>
          </Box>

          {/* Game icons row */}
          <Flex bg="#1a1d27" borderRadius="xl" p={4} borderWidth="1px" borderColor="#2d3148" justify="space-around">
            <VStack gap={1}>
              <MaterialIcon name="forest" style={{ fontSize: 28, color: "#4ade80" }} />
              <Text fontSize="2xs" color="gray.500">Forest</Text>
            </VStack>
            <VStack gap={1}>
              <MaterialIcon name="skull" style={{ fontSize: 28, color: "#f87171" }} />
              <Text fontSize="2xs" color="gray.500">Danger</Text>
            </VStack>
            <VStack gap={1}>
              <MaterialIcon name="person_play" style={{ fontSize: 28, color: "#60a5fa" }} />
              <Text fontSize="2xs" color="gray.500">Player</Text>
            </VStack>
            <VStack gap={1}>
              <MaterialIcon name="house" style={{ fontSize: 28, color: "#f4c025" }} />
              <Text fontSize="2xs" color="gray.500">Exit</Text>
            </VStack>
          </Flex>

          {/* Location */}
          <Box bg="#1a1d27" borderRadius="xl" p={4} borderWidth="1px" borderColor="#2d3148">
            <HStack gap={2} mb={2}>
              <Icon color="#f4c025">
                <LuMapPin />
              </Icon>
              <Text fontSize="sm" fontWeight="600">
                Position
              </Text>
            </HStack>
            <Text fontSize="md" color="gray.300">
              Row {game.player_location[0]}, Col {game.player_location[1]}
            </Text>
          </Box>

          {/* Compass */}
          <Box bg="#1a1d27" borderRadius="xl" p={4} borderWidth="1px" borderColor="#2d3148">
            <HStack gap={2} mb={2}>
              <Icon color="#f4c025">
                <LuCompass />
              </Icon>
              <Text fontSize="sm" fontWeight="600">
                Compass
              </Text>
            </HStack>
            {compass && (
              <HStack gap={2}>
                <Icon fontSize="xl" color={game.compass === "HERE" ? "#4ade80" : "#60a5fa"}>
                  <compass.icon />
                </Icon>
                <Text color={game.compass === "HERE" ? "#4ade80" : "gray.300"} fontWeight="500">
                  {compass.label}
                </Text>
              </HStack>
            )}
          </Box>

          {/* Status badge */}
          {game.finished && (
            <Badge
              size="lg"
              p={3}
              borderRadius="lg"
              textAlign="center"
              bg={game.compass === "HERE" ? "green.900" : "red.900"}
              color={game.compass === "HERE" ? "green.200" : "red.200"}
            >
              {game.compass === "HERE" ? "🎉 You found the exit!" : "Game Over"}
            </Badge>
          )}
        </VStack>

        {/* Right side — Controls + Log */}
        <VStack gap={4} align="stretch">
          {/* Direction controls */}
          <Box bg="#1a1d27" borderRadius="xl" p={5} borderWidth="1px" borderColor="#2d3148">
            <Text fontSize="xs" color="gray.500" fontWeight="600" textTransform="uppercase" mb={4}>
              Controls (or use arrow keys)
            </Text>
            <VStack gap={2}>
              <Button
                w="80px"
                bg="#2d3148"
                color="white"
                _hover={{ bg: "#f4c025", color: "black" }}
                onClick={() => handleMove("N")}
                disabled={game.finished || loading}
              >
                <LuArrowUp /> N
              </Button>
              <HStack gap={2}>
                <Button
                  w="80px"
                  bg="#2d3148"
                  color="white"
                  _hover={{ bg: "#f4c025", color: "black" }}
                  onClick={() => handleMove("W")}
                  disabled={game.finished || loading}
                >
                  <LuArrowLeft /> W
                </Button>
                <Box w="80px" h="40px" display="flex" alignItems="center" justifyContent="center">
                  <Icon fontSize="xl" color="#f4c025">
                    <LuGamepad2 />
                  </Icon>
                </Box>
                <Button
                  w="80px"
                  bg="#2d3148"
                  color="white"
                  _hover={{ bg: "#f4c025", color: "black" }}
                  onClick={() => handleMove("E")}
                  disabled={game.finished || loading}
                >
                  E <LuArrowRight />
                </Button>
              </HStack>
              <Button
                w="80px"
                bg="#2d3148"
                color="white"
                _hover={{ bg: "#f4c025", color: "black" }}
                onClick={() => handleMove("S")}
                disabled={game.finished || loading}
              >
                <LuArrowDown /> S
              </Button>
            </VStack>
          </Box>

          {/* Game log */}
          <Box
            bg="#1a1d27"
            borderRadius="xl"
            p={5}
            borderWidth="1px"
            borderColor="#2d3148"
            flex={1}
            minH="300px"
            maxH="450px"
            overflowY="auto"
          >
            <Text fontSize="xs" color="gray.500" fontWeight="600" textTransform="uppercase" mb={3}>
              Game Log
            </Text>
            <VStack gap={1} align="stretch">
              {game.messages.map((msg, i) => (
                <HStack key={i} gap={2} py={1} borderBottomWidth="1px" borderColor="#2d3148">
                  <Text fontSize="xs" color="gray.600" whiteSpace="nowrap">
                    [{String(i + 1).padStart(2, "0")}]
                  </Text>
                  <Text fontSize="sm" color={msg.includes("***") ? "#4ade80" : msg.includes("-") ? "#f87171" : "gray.300"}>
                    {msg}
                  </Text>
                </HStack>
              ))}
              <div ref={logEndRef} />
            </VStack>
          </Box>

          {error && (
            <Text color="red.400" fontSize="sm">
              {error}
            </Text>
          )}
        </VStack>
      </Grid>
    </Container>
  );
}
