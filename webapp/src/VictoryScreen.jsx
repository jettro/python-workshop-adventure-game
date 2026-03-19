import {
  Box,
  Button,
  Flex,
  Heading,
  HStack,
  Icon,
  Text,
  VStack,
} from "@chakra-ui/react";
import { LuPlay, LuHouse } from "react-icons/lu";

function MaterialIcon({ name, ...props }) {
  return (
    <span className="material-icons" {...props}>
      {name}
    </span>
  );
}

function StatCard({ icon, iconColor, label, value }) {
  return (
    <Box
      bg="#1a1d27"
      borderRadius="xl"
      p={6}
      borderWidth="1px"
      borderColor="#2d3148"
      textAlign="center"
      flex={1}
      minW="160px"
    >
      <Flex justify="center" mb={3}>
        <Box
          bg={`${iconColor}20`}
          borderRadius="full"
          w="56px"
          h="56px"
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <MaterialIcon name={icon} style={{ fontSize: 28, color: iconColor }} />
        </Box>
      </Flex>
      <Text fontSize="xs" color="gray.500" fontWeight="600" textTransform="uppercase" mb={1}>
        {label}
      </Text>
      <Heading size="2xl" color="white" fontWeight="bold">
        {value}
      </Heading>
    </Box>
  );
}

function AchievementBadge({ icon, label }) {
  return (
    <HStack
      bg="#1a1d27"
      borderRadius="lg"
      px={4}
      py={3}
      borderWidth="1px"
      borderColor="#2d3148"
      gap={3}
    >
      <MaterialIcon name={icon} style={{ fontSize: 22, color: "#f4c025" }} />
      <Text fontSize="sm" fontWeight="500" color="gray.200">
        {label}
      </Text>
    </HStack>
  );
}

export default function VictoryScreen({ game, onPlayAgain, onReturnToMenu }) {
  // Derive stats from game state
  const totalMoves = game.messages.length - 1; // exclude welcome message
  const charactersFound = game.messages.filter((m) => m.includes("Character found")).length;

  // Determine achievements based on gameplay
  const achievements = [];
  if (totalMoves <= 15) {
    achievements.push({ icon: "sprint", label: "Speedrunner" });
  }
  if (game.score >= 150) {
    achievements.push({ icon: "shield", label: "Untouchable" });
  }
  if (charactersFound >= 1) {
    achievements.push({ icon: "lock", label: "Treasure Hunter" });
  }
  if (game.score >= 100) {
    achievements.push({ icon: "star", label: "High Scorer" });
  }

  return (
    <Flex minH="100vh" align="center" justify="center" direction="column" px={4}>
      <VStack gap={8} maxW="700px" w="full">
        {/* Trophy icon */}
        <Box
          bg="#f4c02520"
          borderRadius="full"
          w="120px"
          h="120px"
          display="flex"
          alignItems="center"
          justifyContent="center"
          boxShadow="0 0 60px #f4c02530"
        >
          <MaterialIcon name="military_tech" style={{ fontSize: 64, color: "#f4c025" }} />
        </Box>

        {/* Title */}
        <VStack gap={2}>
          <Heading size="4xl" fontWeight="bold" color="#f4c025">
            Victory!
          </Heading>
          <Text color="gray.400" fontSize="lg" textAlign="center">
            You found the exit and escaped the darkness!
          </Text>
        </VStack>

        {/* Stat cards */}
        <Flex
          gap={4}
          w="full"
          direction={{ base: "column", sm: "row" }}
          justify="center"
        >
          <StatCard
            icon="military_tech"
            iconColor="#f4c025"
            label="Final Score"
            value={game.score.toLocaleString()}
          />
          <StatCard
            icon="timer"
            iconColor="#60a5fa"
            label="Moves Made"
            value={totalMoves}
          />
          <StatCard
            icon="skull"
            iconColor="#f87171"
            label="Characters Found"
            value={charactersFound}
          />
        </Flex>

        {/* Achievements */}
        {achievements.length > 0 && (
          <Box w="full">
            <HStack gap={2} mb={3} justify="center">
              <MaterialIcon name="stars" style={{ fontSize: 20, color: "#f4c025" }} />
              <Heading size="md" fontWeight="600" color="gray.200">
                Achievements Unlocked
              </Heading>
            </HStack>
            <Flex gap={3} wrap="wrap" justify="center">
              {achievements.map((a) => (
                <AchievementBadge key={a.label} icon={a.icon} label={a.label} />
              ))}
            </Flex>
          </Box>
        )}

        {/* Action buttons */}
        <HStack gap={4} pt={2}>
          <Button
            size="lg"
            bg="#f4c025"
            color="black"
            _hover={{ bg: "#d4a520" }}
            onClick={onPlayAgain}
          >
            <Icon mr={1}>
              <LuPlay />
            </Icon>
            Play Again
          </Button>
          <Button
            size="lg"
            variant="outline"
            borderColor="#2d3148"
            color="gray.300"
            _hover={{ bg: "#1a1d27" }}
            onClick={onReturnToMenu}
          >
            <Icon mr={1}>
              <LuHouse />
            </Icon>
            Return to Menu
          </Button>
        </HStack>
      </VStack>
    </Flex>
  );
}
