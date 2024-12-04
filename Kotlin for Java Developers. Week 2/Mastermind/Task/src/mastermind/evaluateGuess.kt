package mastermind

data class Evaluation(val rightPosition: Int, val wrongPosition: Int)

fun evaluateGuess(secret: String, guess: String): Evaluation {
    val rightIndexes = mutableListOf<Int>()

    for (it in guess.withIndex()) {
        if (it.value == secret[it.index]) {
            rightIndexes.add(it.index)
        }
    }

    val rightPosition = rightIndexes.size
    var wrongPosition = 0

    val usedIndexes = ArrayList(rightIndexes)
    for (it in guess.withIndex()) {
        if (it.index !in rightIndexes) {
            val wIndex = findMatchingIndex(it.value, secret, usedIndexes)
            if (wIndex != null) {
                usedIndexes.add(wIndex)
                wrongPosition++
            }
        }
    }

    return Evaluation(rightPosition, wrongPosition)
}

fun findMatchingIndex(value: Char, secret: String, usedIndexes: MutableList<Int>): Int? {
    for (it in secret.withIndex()) {
        if (it.index !in usedIndexes && it.value == value) {
            return it.index
        }
    }

    return null
}




