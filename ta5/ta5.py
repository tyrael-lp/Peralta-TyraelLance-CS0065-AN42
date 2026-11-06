import textblob as tb

while True:
    continue_input = input("\nDo you want to analyze a sentence? (yes/no): ")
    if continue_input.lower() != "yes":
        break
    sentence = input("Enter a sentence: ")
    blob = tb.TextBlob(sentence)

    if blob.sentiment.polarity < 0:
        print("The sentiment of the sentence is negative.")
    elif blob.sentiment.polarity > 0:
        print("The sentiment of the sentence is positive.")
    else:
        print("The sentiment of the sentence is neutral.")