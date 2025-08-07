import random
import csv

class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.count = 0

    def addsong(self, song):
        new_node = Node(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = self.head
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.count += 1

    def removesongindex(self, index):
        if not self.head:
            print("NO SONGS PRESENT")
            return

        if index < 0 or index >= self.count:
            print("INVALID INDEX")
            return

        current = self.head
        if index == 0:
            self.head = current.next
            if self.head:
                self.head.prev = None
            if self.head is None:
                self.tail = None
        else:
            for i in range(index):
                current = current.next
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == self.tail:
                self.tail = current.prev
        self.count -= 1
        print(f"Removed song at index {index}.")

    def removesongname(self, song):
      if not self.head:
        print("NO SONGS PRESENT")
        return
      current = self.head
      while current:
        if current.song == song:
          if current.prev:
            current.prev.next = current.next
          if current.next:
            current.next.prev = current.prev
          if current == self.head:
            self.head = current.next
          if current == self.tail:
            self.tail = current.prev
          self.count -= 1
          print(f"Removed '{song}' from the playlist.")
          return
        current = current.next
      print(f"Song '{song}' not found in the playlist.")

    def display_playlist(self):
        if not self.head:
            print("The playlist is empty.")
            return

        current = self.head
        print("--- My Music Playlist ---")
        print("-" * 30)
        index = 1
        while current:
            print(f"{index}. {current.song}")
            current = current.next
            index += 1
        print("-" * 30)
        print(f"Total Songs: {self.count}")

    def shuffle_playlist(self):
        if self.count <= 1:
            return
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        random.shuffle(nodes)
        self.head = nodes[0]
        current = self.head
        for node in nodes[1:]:
            current.next = node
            node.prev = current
            current = node
        current.next = None
        self.tail = current

    def repeatsong(self, song):
        if self.count <= 0:
            print("NO SONG TO REPEAT")
            return
        current = self.head
        while current:
            if current.song == song:
                cuthead = current.next
                current.next = current
                print(f"Repeating: {current.song}")
                print("To stop repeating, Enter 1:")
                while True:
                    n = int(input())
                    if n == 1:
                        current.next = cuthead
                        print("REPEAT STOPPED")
                        break
                    else:
                        print("INVALID INPUT")
            current = current.next

    def repeatplaylist(self):
        if self.head is None:
            print("NO SONG IN PLAYLIST")
            return
        self.tail.next = self.head
        self.head.prev = self.tail

    def searchsong(self, song):
        if self.count < 1:
            print("NO SONG IN PLAYLIST")
            return
        current = self.head
        while current:
            if current.song == song:
                print("SONG:", song, "Found")
                return
            current = current.next
        print('SONG:', song, "NOT FOUND")

    def play(self):
        if not self.current:
            print("NO SONG TO PLAY")
            return
        print("Playing:", self.current.song)

    def skip(self):
        if not self.current or not self.current.next:
            print("NO MORE SONGS TO SKIP")
            return
        self.current = self.current.next
        print("Skipping to:", self.current.song)

    def previous(self):
        if not self.current or not self.current.prev:
            print("NO PREVIOUS SONG TO PLAY")
            return
        self.current = self.current.prev
        print("Going back to:", self.current.song)

    def save_to_csv(self, filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Song"])
            current = self.head
            while current:
                writer.writerow([current.song])
                current = current.next
def main():
    print("Welcome to the Music Playlist Manager!")
    playlist_name = input("Please enter a name for your playlist: ")
    filename = f"{playlist_name}.csv"

    playlist = MusicPlaylist()

    while True:
        print(f"\n--- {playlist_name} Menu ---")
        print("1. Add Song")
        print("2. Remove Song")
        print("3. Display Playlist")
        print("4. Shuffle Playlist")
        print("5. Play Current Song")
        print("6. Skip to Next Song")
        print("7. Go Back to Previous Song")
        print("8. Repeat a Song")
        print("9. Repeat Playlist")
        print("10. Search for a Song")
        print("11. Save Playlist to CSV")
        print("12. Exit")
        choice = input("Enter your choice (1-14): ")

        match(choice):
            case '1':
                song = input("Enter the song name: ")
                playlist.addsong(song)
                print(f"Added '{song}' to the playlist.")
            case '2':
                remove_choice = input("Remove by (n)ame or (i)ndex? ").lower()
                if remove_choice == 'i':
                    index = int(input("Enter the index of the song to remove: "))
                    playlist.removesongindex(index - 1)
                elif remove_choice == 'n':
                    song = input("Enter the name of the song to remove: ")
                    playlist.removesongname(song)
                else:
                    print("Invalid choice. Please enter 'n' or 'i'.")
            case '3':
                playlist.display_playlist()
            case '4':
                playlist.shuffle_playlist()
                print("Playlist shuffled.")
            case '5':
                playlist.play()
            case '6':
                playlist.skip()
            case '7':
                playlist.previous()
            case '8':
                song = input("Enter the song name to repeat: ")
                playlist.repeatsong(song)
            case '9':
                playlist.repeatplaylist()
            case '10':
                song = input("Enter the song name to search: ")
                playlist.searchsong(song)
            case '11':
                playlist.save_to_csv(filename)
                print(f"Playlist saved to {filename}.")
            case '12':
                print("Exiting the program. Goodbye!")
                break
            case _:
                print("Invalid choice, select a valid option.")
main()