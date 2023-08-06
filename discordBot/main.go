package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
)

/**
 * TODO - need to add a start game prompt
 */

func main() {
	session, err := discordgo.New("Bot " + "MTEzNTc2MjE3MTQ1MjcyMzM1MA.GbiUpU.nXUzwViJCMtEhDMIiIC9impGAc55CRgTBiaffM")
	if err != nil {
		log.Fatal((err))
	}

	//fmt.Println(session)

	// accepts another function as its parameter
	session.AddHandler(func(s *discordgo.Session, m *discordgo.MessageCreate) {
		if m.Author.ID == s.State.User.ID {
			return
		}

		// check sent message
		fmt.Println("message from user: " + m.Content)
		if m.Content == "rock" {

			// send message from bot
			s.ChannelMessageSend(m.ChannelID, "paper")
		} else if m.Content == "paper" {
			s.ChannelMessageSend(m.ChannelID, "scissor")
		} else if m.Content == "scissor" {
			s.ChannelMessageSend(m.ChannelID, "rock")
		} else {
			s.ChannelMessageSend(m.ChannelID, "incorrect input")
		}
	})

	session.Identify.Intents = discordgo.IntentsAllWithoutPrivileged

	err = session.Open()
	if err != nil {
		log.Fatal(err)
	}

	defer session.Close()

	fmt.Println("the bot is online!")

	// lock the thread
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc
}
