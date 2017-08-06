

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost1 = self.addHost( 'h1' )
		leftHost2 = self.addHost( 'h3' )
        rightHost1 = self.addHost( 'h2' )
		rightHost2 = self.addHost( 'h4' )
		rightHost3 = self.addHost( 'h5' )
		rightHost4 = self.addHost( 'h6' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost1, leftSwitch )
		self.addLink( leftHost2, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost1 )
		self.addLink( rightSwitch, rightHost2 )
		self.addLink( rightSwitch, rightHost3 )
		self.addLink( rightSwitch, rightHost4 )


topos = { 'mytopo': ( lambda: MyTopo() ) }
