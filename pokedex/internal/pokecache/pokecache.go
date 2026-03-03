package pokecache

import (
	"sync"
	"time"
)

type Cache struct {
	entries map[string]cacheEntry
	mutex   sync.Mutex
	done    chan struct{}
}

type cacheEntry struct {
	createdAt time.Time
	val       []byte
}

func NewCache(interval time.Duration) *Cache {
	cache := &Cache{
		entries: make(map[string]cacheEntry),
		done:    make(chan struct{}),
	}

	go func() {
		ticker := time.NewTicker(interval)
		defer ticker.Stop()

		for {
			select {
			case <-ticker.C:
				cache.reapLoop(interval)
			case <-cache.done:
				return
			}
		}
	}()

	return cache
}

func (c *Cache) reapLoop(interval time.Duration) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	for k, v := range c.entries {
		if time.Since(v.createdAt) > interval {
			delete(c.entries, k)
		}
	}
}

func (c *Cache) Add(key string, val []byte) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	c.entries[key] = cacheEntry{createdAt: time.Now(), val: val}
}

func (c *Cache) Get(key string) ([]byte, bool) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	entry, exists := c.entries[key]

	return entry.val, exists
}

func (c *Cache) Close() {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	close(c.done)
}
