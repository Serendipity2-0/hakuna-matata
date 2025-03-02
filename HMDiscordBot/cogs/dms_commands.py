"""
Document Management System (DMS) commands for the Discord bot.
This module implements Discord commands for managing markdown files in the DMS database.
"""

import os
import logging
import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dms_commands')

class DMSCommands(commands.Cog):
    """
    Discord commands for managing markdown files in the DMS database.
    
    This cog provides commands for uploading, viewing, querying, and updating documents.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the DMS commands.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        
        # Get the database path
        base_dir = os.getcwd()
        self.db_path = os.path.join(base_dir, "DB", "Main", "dms.db")
        self.dms_folder = os.path.join(base_dir, "DMS")
        
        # Ensure the DMS folder exists
        os.makedirs(self.dms_folder, exist_ok=True)
        
        # Define the available departments
        self.departments = [
            "Development", "Marketing", "Accounts", "HR", "Operations", "Sales", "Other"
        ]
        
        logger.info("DMS commands initialized")
        logger.info(f"DMS folder path: {self.dms_folder}")
        logger.info(f"DMS database path: {self.db_path}")
    
    def get_db_connection(self):
        """
        Get a connection to the DMS database.
        
        Returns:
            sqlite3.Connection: A connection to the DMS database
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler that runs when the cog is loaded."""
        logger.info("DMS commands cog is ready")
    
    # ===== Prefix Commands =====
    
    @commands.command(name="dms_help")
    async def dms_help(self, ctx: commands.Context):
        """Display help information for DMS commands."""
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Document Management System Commands",
            description="Here are the available DMS commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}dms_help` - Show this help message\n"
                f"`{prefix}upload_document` - Upload a new document (interactive)\n"
                f"`{prefix}view_documents` - View all documents\n"
                f"`{prefix}search_document [query]` - Search for documents\n"
                f"`{prefix}update_document [id]` - Update a document (interactive)\n"
                f"`{prefix}download_document [id]` - Download a document"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/dms_help` - Show this help message\n"
                "`/upload_document` - Upload a new document\n"
                "`/view_documents` - View all documents\n"
                "`/search_document` - Search for documents\n"
                "`/update_document` - Update a document\n"
                "`/download_document` - Download a document"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await ctx.send(embed=help_embed)
    
    @commands.command(name="upload_document")
    async def upload_document_prefix(self, ctx: commands.Context):
        """Upload a new document to the DMS (interactive)."""
        await ctx.send("Please use the `/upload_document` slash command to upload a document with a form.")
    
    @commands.command(name="view_documents")
    async def view_documents_prefix(self, ctx: commands.Context):
        """View all documents in the DMS."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DMS ORDER BY docid DESC")
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                await ctx.send("No documents found in the DMS.")
                return
            
            # Create a paginator for the documents
            paginator = DocumentPaginator(ctx, documents, "All Documents")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error viewing documents: {str(e)}", exc_info=True)
            await ctx.send(f"Error viewing documents: {str(e)}")
    
    @commands.command(name="search_document")
    async def search_document_prefix(self, ctx: commands.Context, *, query: str = None):
        """
        Search for documents in the DMS.
        
        Args:
            query: Search query
        """
        if not query:
            await ctx.send("Please provide a search query.")
            return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Search in name, tags, description, and department
            cursor.execute("""
                SELECT * FROM DMS 
                WHERE name LIKE ? OR tags LIKE ? OR description LIKE ? OR department LIKE ?
                ORDER BY docid DESC
            """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                await ctx.send(f"No documents found matching '{query}'.")
                return
            
            # Create a paginator for the documents
            paginator = DocumentPaginator(ctx, documents, f"Search Results for '{query}'")
            await paginator.start()
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}", exc_info=True)
            await ctx.send(f"Error searching documents: {str(e)}")
    
    @commands.command(name="update_document")
    async def update_document_prefix(self, ctx: commands.Context, doc_id: int = None):
        """
        Update a document in the DMS.
        
        Args:
            doc_id: The ID of the document to update
        """
        if not doc_id:
            await ctx.send("Please provide a document ID to update.")
            return
        
        await ctx.send("Please use the `/update_document` slash command to update a document with a form.")
    
    @commands.command(name="download_document")
    async def download_document_prefix(self, ctx: commands.Context, doc_id: int = None):
        """
        Download a document from the DMS.
        
        Args:
            doc_id: The ID of the document to download
        """
        if not doc_id:
            await ctx.send("Please provide a document ID to download.")
            return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DMS WHERE docid = ?", (doc_id,))
            document = cursor.fetchone()
            conn.close()
            
            if not document:
                await ctx.send(f"Document with ID {doc_id} not found.")
                return
            
            # Check if the document file exists
            doc_path = os.path.join(self.dms_folder, f"{doc_id}_{document['name']}.md")
            if not os.path.exists(doc_path):
                await ctx.send(f"Document file not found for ID {doc_id}.")
                return
            
            # Read the document file
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create a file to send
            file = discord.File(
                io.BytesIO(content.encode("utf-8")),
                filename=f"{document['name']}.md"
            )
            
            # Create an embed with document info
            embed = discord.Embed(
                title=f"Document: {document['name']}",
                description=document['description'],
                color=discord.Color.blue()
            )
            
            embed.add_field(name="ID", value=document['docid'], inline=True)
            embed.add_field(name="Department", value=document['department'], inline=True)
            embed.add_field(name="Tags", value=document['tags'] or "None", inline=True)
            
            await ctx.send(embed=embed, file=file)
            
        except Exception as e:
            logger.error(f"Error downloading document: {str(e)}", exc_info=True)
            await ctx.send(f"Error downloading document: {str(e)}")
    
    # ===== Slash Commands =====
    
    @app_commands.command(name="dms_help", description="Display help information for DMS commands")
    async def dms_help_slash(self, interaction: discord.Interaction):
        """Display help information for DMS commands."""
        prefix = self.bot.command_prefix
        
        help_embed = discord.Embed(
            title="Document Management System Commands",
            description="Here are the available DMS commands:",
            color=discord.Color.blue()
        )
        
        help_embed.add_field(
            name="Prefix Commands",
            value=(
                f"`{prefix}dms_help` - Show this help message\n"
                f"`{prefix}upload_document` - Upload a new document (interactive)\n"
                f"`{prefix}view_documents` - View all documents\n"
                f"`{prefix}search_document [query]` - Search for documents\n"
                f"`{prefix}update_document [id]` - Update a document (interactive)\n"
                f"`{prefix}download_document [id]` - Download a document"
            ),
            inline=False
        )
        
        help_embed.add_field(
            name="Slash Commands",
            value=(
                "`/dms_help` - Show this help message\n"
                "`/upload_document` - Upload a new document\n"
                "`/view_documents` - View all documents\n"
                "`/search_document` - Search for documents\n"
                "`/update_document` - Update a document\n"
                "`/download_document` - Download a document"
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Use the buttons and dropdowns in responses for easier interaction")
        
        await interaction.response.send_message(embed=help_embed, ephemeral=True)
    
    @app_commands.command(name="upload_document", description="Upload a new document to the DMS")
    async def upload_document_slash(self, interaction: discord.Interaction):
        """Upload a new document to the DMS."""
        # Create a modal for uploading a document
        modal = UploadDocumentModal(self)
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="view_documents", description="View all documents in the DMS")
    async def view_documents_slash(self, interaction: discord.Interaction):
        """View all documents in the DMS."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DMS ORDER BY docid DESC")
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                await interaction.response.send_message("No documents found in the DMS.")
                return
            
            # Create a paginator for the documents
            paginator = DocumentPaginatorView(documents, "All Documents")
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error viewing documents: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error viewing documents: {str(e)}")
    
    @app_commands.command(name="search_document", description="Search for documents in the DMS")
    @app_commands.describe(query="Search query")
    async def search_document_slash(self, interaction: discord.Interaction, query: str):
        """
        Search for documents in the DMS.
        
        Args:
            query: Search query
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Search in name, tags, description, and department
            cursor.execute("""
                SELECT * FROM DMS 
                WHERE name LIKE ? OR tags LIKE ? OR description LIKE ? OR department LIKE ?
                ORDER BY docid DESC
            """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                await interaction.response.send_message(f"No documents found matching '{query}'.")
                return
            
            # Create a paginator for the documents
            paginator = DocumentPaginatorView(documents, f"Search Results for '{query}'")
            
            # Send the first page
            await interaction.response.send_message(
                embed=paginator.get_page_embed(),
                view=paginator
            )
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error searching documents: {str(e)}")
    
    @app_commands.command(name="update_document", description="Update a document in the DMS")
    @app_commands.describe(doc_id="The ID of the document to update")
    async def update_document_slash(self, interaction: discord.Interaction, doc_id: int):
        """
        Update a document in the DMS.
        
        Args:
            doc_id: The ID of the document to update
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DMS WHERE docid = ?", (doc_id,))
            document = cursor.fetchone()
            conn.close()
            
            if not document:
                await interaction.response.send_message(f"Document with ID {doc_id} not found.", ephemeral=True)
                return
            
            # Check if the document file exists
            doc_path = os.path.join(self.dms_folder, f"{doc_id}_{document['name']}.md")
            if not os.path.exists(doc_path):
                # Create an empty file if it doesn't exist
                with open(doc_path, "w", encoding="utf-8") as f:
                    f.write("")
            
            # Read the document file
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create a modal for updating the document
            modal = UpdateDocumentModal(self, document, content)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating document: {str(e)}")
    
    @app_commands.command(name="download_document", description="Download a document from the DMS")
    @app_commands.describe(doc_id="The ID of the document to download")
    async def download_document_slash(self, interaction: discord.Interaction, doc_id: int):
        """
        Download a document from the DMS.
        
        Args:
            doc_id: The ID of the document to download
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DMS WHERE docid = ?", (doc_id,))
            document = cursor.fetchone()
            conn.close()
            
            if not document:
                await interaction.response.send_message(f"Document with ID {doc_id} not found.", ephemeral=True)
                return
            
            # Check if the document file exists
            doc_path = os.path.join(self.dms_folder, f"{doc_id}_{document['name']}.md")
            if not os.path.exists(doc_path):
                await interaction.response.send_message(f"Document file not found for ID {doc_id}.", ephemeral=True)
                return
            
            # Read the document file
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create a file to send
            file = discord.File(
                io.BytesIO(content.encode("utf-8")),
                filename=f"{document['name']}.md"
            )
            
            # Create an embed with document info
            embed = discord.Embed(
                title=f"Document: {document['name']}",
                description=document['description'],
                color=discord.Color.blue()
            )
            
            embed.add_field(name="ID", value=document['docid'], inline=True)
            embed.add_field(name="Department", value=document['department'], inline=True)
            embed.add_field(name="Tags", value=document['tags'] or "None", inline=True)
            
            await interaction.response.send_message(embed=embed, file=file)
            
        except Exception as e:
            logger.error(f"Error downloading document: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error downloading document: {str(e)}")


# ===== UI Components =====

class UploadDocumentModal(discord.ui.Modal, title="Upload Document"):
    """Modal for uploading a new document to the DMS."""
    
    def __init__(self, cog: DMSCommands):
        super().__init__()
        self.cog = cog
        
        # Create the form fields
        self.name_input = discord.ui.TextInput(
            label="Document Name",
            placeholder="e.g., Project Guidelines",
            required=True,
            max_length=100
        )
        self.add_item(self.name_input)
        
        self.tags_input = discord.ui.TextInput(
            label="Tags (comma-separated)",
            placeholder="e.g., guidelines, project, development",
            required=False,
            max_length=100
        )
        self.add_item(self.tags_input)
        
        self.description_input = discord.ui.TextInput(
            label="Description",
            placeholder="Brief description of the document",
            required=True,
            style=discord.TextStyle.paragraph,
            max_length=200
        )
        self.add_item(self.description_input)
        
        self.department_input = discord.ui.TextInput(
            label="Department",
            placeholder="e.g., Development, Marketing, Accounts",
            required=True,
            max_length=50
        )
        self.add_item(self.department_input)
        
        self.content_input = discord.ui.TextInput(
            label="Document Content (Markdown)",
            placeholder="# Your Markdown Content Here\n\nWrite your document content using Markdown syntax.",
            required=True,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.content_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Get the current timestamp
            now = datetime.now().strftime("%Y-%m-%d")
            
            # Create the document data
            document_data = {
                "name": self.name_input.value,
                "tags": self.tags_input.value,
                "description": self.description_input.value,
                "created_at": now,
                "department": self.department_input.value,
                "created_by": interaction.user.name,
                "updated_by": interaction.user.name,
                "comments": "",
                "last_updated_at": now
            }
            
            # Insert the document into the database
            conn = self.cog.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO DMS (
                    name, tags, description, created_at, department, 
                    created_by, updated_by, comments, last_updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                document_data["name"], document_data["tags"], document_data["description"],
                document_data["created_at"], document_data["department"],
                document_data["created_by"], document_data["updated_by"],
                document_data["comments"], document_data["last_updated_at"]
            ))
            
            # Get the document ID
            doc_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Save the document content to a file
            doc_path = os.path.join(self.cog.dms_folder, f"{doc_id}_{document_data['name']}.md")
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(self.content_input.value)
            
            # Create a success embed
            embed = discord.Embed(
                title="Document Uploaded Successfully",
                description=f"Document #{doc_id} has been uploaded to the DMS.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Name", value=document_data["name"], inline=True)
            embed.add_field(name="Department", value=document_data["department"], inline=True)
            embed.add_field(name="Tags", value=document_data["tags"] or "None", inline=True)
            
            # Create a view with a download button
            view = discord.ui.View()
            download_button = discord.ui.Button(
                label="Download Document",
                style=discord.ButtonStyle.primary,
                custom_id=f"download_{doc_id}"
            )
            
            async def download_callback(interaction: discord.Interaction):
                await self.cog.download_document_slash(interaction, doc_id)
            
            download_button.callback = download_callback
            view.add_item(download_button)
            
            await interaction.response.send_message(embed=embed, view=view)
            
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error uploading document: {str(e)}")


class UpdateDocumentModal(discord.ui.Modal, title="Update Document"):
    """Modal for updating an existing document in the DMS."""
    
    def __init__(self, cog: DMSCommands, document: sqlite3.Row, content: str):
        super().__init__()
        self.cog = cog
        self.document = document
        self.doc_id = document["docid"]
        
        # Create the form fields with current values
        self.name_input = discord.ui.TextInput(
            label="Document Name",
            placeholder="e.g., Project Guidelines",
            required=True,
            max_length=100,
            default=document["name"]
        )
        self.add_item(self.name_input)
        
        self.tags_input = discord.ui.TextInput(
            label="Tags (comma-separated)",
            placeholder="e.g., guidelines, project, development",
            required=False,
            max_length=100,
            default=document["tags"] or ""
        )
        self.add_item(self.tags_input)
        
        self.description_input = discord.ui.TextInput(
            label="Description",
            placeholder="Brief description of the document",
            required=True,
            style=discord.TextStyle.paragraph,
            max_length=200,
            default=document["description"] or ""
        )
        self.add_item(self.description_input)
        
        self.department_input = discord.ui.TextInput(
            label="Department",
            placeholder="e.g., Development, Marketing, Accounts",
            required=True,
            max_length=50,
            default=document["department"] or ""
        )
        self.add_item(self.department_input)
        
        self.content_input = discord.ui.TextInput(
            label="Document Content (Markdown)",
            placeholder="# Your Markdown Content Here\n\nWrite your document content using Markdown syntax.",
            required=True,
            style=discord.TextStyle.paragraph,
            default=content
        )
        self.add_item(self.content_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission."""
        try:
            # Get the current timestamp
            now = datetime.now().strftime("%Y-%m-%d")
            
            # Create the document data
            document_data = {
                "name": self.name_input.value,
                "tags": self.tags_input.value,
                "description": self.description_input.value,
                "department": self.department_input.value,
                "updated_by": interaction.user.name,
                "last_updated_at": now
            }
            
            # Update the document in the database
            conn = self.cog.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE DMS SET
                    name = ?, tags = ?, description = ?, department = ?,
                    updated_by = ?, last_updated_at = ?
                WHERE docid = ?
            """, (
                document_data["name"], document_data["tags"], document_data["description"],
                document_data["department"], document_data["updated_by"],
                document_data["last_updated_at"], self.doc_id
            ))
            
            conn.commit()
            conn.close()
            
            # Check if the old document file exists and remove it if the name changed
            old_doc_path = os.path.join(self.cog.dms_folder, f"{self.doc_id}_{self.document['name']}.md")
            new_doc_path = os.path.join(self.cog.dms_folder, f"{self.doc_id}_{document_data['name']}.md")
            
            if old_doc_path != new_doc_path and os.path.exists(old_doc_path):
                os.remove(old_doc_path)
            
            # Save the document content to a file
            with open(new_doc_path, "w", encoding="utf-8") as f:
                f.write(self.content_input.value)
            
            # Create a success embed
            embed = discord.Embed(
                title="Document Updated Successfully",
                description=f"Document #{self.doc_id} has been updated in the DMS.",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Name", value=document_data["name"], inline=True)
            embed.add_field(name="Department", value=document_data["department"], inline=True)
            embed.add_field(name="Tags", value=document_data["tags"] or "None", inline=True)
            
            # Create a view with a download button
            view = discord.ui.View()
            download_button = discord.ui.Button(
                label="Download Document",
                style=discord.ButtonStyle.primary,
                custom_id=f"download_{self.doc_id}"
            )
            
            async def download_callback(interaction: discord.Interaction):
                await self.cog.download_document_slash(interaction, self.doc_id)
            
            download_button.callback = download_callback
            view.add_item(download_button)
            
            await interaction.response.send_message(embed=embed, view=view)
            
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"Error updating document: {str(e)}")


class DocumentPaginator:
    """Paginator for displaying documents in a paginated manner (for prefix commands)."""
    
    def __init__(self, ctx: commands.Context, documents: List[sqlite3.Row], title: str):
        """
        Initialize the paginator.
        
        Args:
            ctx: The command context
            documents: List of documents to paginate
            title: Title for the paginator
        """
        self.ctx = ctx
        self.documents = documents
        self.title = title
        self.page = 0
        self.total_pages = len(documents)
        
    async def start(self):
        """Start the paginator."""
        if not self.documents:
            await self.ctx.send("No documents to display.")
            return
        
        # Create the message with the first page
        self.message = await self.ctx.send(embed=self.get_page_embed(), view=self.get_page_view())
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        document = self.documents[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            description=document["description"],
            color=discord.Color.blue()
        )
        
        # Add document details to the embed
        embed.add_field(name="ID", value=document["docid"], inline=True)
        embed.add_field(name="Name", value=document["name"], inline=True)
        embed.add_field(name="Department", value=document["department"], inline=True)
        
        embed.add_field(name="Tags", value=document["tags"] or "None", inline=True)
        embed.add_field(name="Created By", value=document["created_by"], inline=True)
        embed.add_field(name="Created At", value=document["created_at"], inline=True)
        
        embed.add_field(name="Updated By", value=document["updated_by"], inline=True)
        embed.add_field(name="Last Updated At", value=document["last_updated_at"], inline=True)
        
        if document["comments"]:
            embed.add_field(name="Comments", value=document["comments"], inline=False)
        
        return embed
    
    def get_page_view(self) -> discord.ui.View:
        """Get the view for the current page."""
        view = discord.ui.View(timeout=60)
        
        # Previous button
        previous_button = discord.ui.Button(
            label="Previous",
            style=discord.ButtonStyle.gray,
            disabled=self.page == 0,
            custom_id="previous"
        )
        previous_button.callback = self.previous_page
        view.add_item(previous_button)
        
        # Next button
        next_button = discord.ui.Button(
            label="Next",
            style=discord.ButtonStyle.gray,
            disabled=self.page == self.total_pages - 1,
            custom_id="next"
        )
        next_button.callback = self.next_page
        view.add_item(next_button)
        
        # Download button
        download_button = discord.ui.Button(
            label="Download",
            style=discord.ButtonStyle.primary,
            custom_id=f"download_{self.documents[self.page]['docid']}"
        )
        download_button.callback = self.download_document
        view.add_item(download_button)
        
        return view
    
    async def previous_page(self, interaction: discord.Interaction):
        """Go to the previous page."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        self.page = max(0, self.page - 1)
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self.get_page_view())
    
    async def next_page(self, interaction: discord.Interaction):
        """Go to the next page."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        self.page = min(self.total_pages - 1, self.page + 1)
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self.get_page_view())
    
    async def download_document(self, interaction: discord.Interaction):
        """Download the current document."""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This pagination is not for you.", ephemeral=True)
            return
        
        document = self.documents[self.page]
        doc_id = document["docid"]
        
        # Defer the response to avoid timeout
        await interaction.response.defer()
        
        # Call the download command
        await self.ctx.invoke(self.ctx.bot.get_command("download_document"), doc_id=doc_id)


class DocumentPaginatorView(discord.ui.View):
    """Paginator view for displaying documents in a paginated manner (for slash commands)."""
    
    def __init__(self, documents: List[sqlite3.Row], title: str):
        """
        Initialize the paginator view.
        
        Args:
            documents: List of documents to paginate
            title: Title for the paginator
        """
        super().__init__(timeout=60)
        self.documents = documents
        self.title = title
        self.page = 0
        self.total_pages = len(documents)
    
    def get_page_embed(self) -> discord.Embed:
        """Get the embed for the current page."""
        document = self.documents[self.page]
        
        embed = discord.Embed(
            title=f"{self.title} (Page {self.page + 1}/{self.total_pages})",
            description=document["description"],
            color=discord.Color.blue()
        )
        
        # Add document details to the embed
        embed.add_field(name="ID", value=document["docid"], inline=True)
        embed.add_field(name="Name", value=document["name"], inline=True)
        embed.add_field(name="Department", value=document["department"], inline=True)
        
        embed.add_field(name="Tags", value=document["tags"] or "None", inline=True)
        embed.add_field(name="Created By", value=document["created_by"], inline=True)
        embed.add_field(name="Created At", value=document["created_at"], inline=True)
        
        embed.add_field(name="Updated By", value=document["updated_by"], inline=True)
        embed.add_field(name="Last Updated At", value=document["last_updated_at"], inline=True)
        
        if document["comments"]:
            embed.add_field(name="Comments", value=document["comments"], inline=False)
        
        return embed
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the previous page."""
        self.page = max(0, self.page - 1)
        
        # Update the button states
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.total_pages - 1
        
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go to the next page."""
        self.page = min(self.total_pages - 1, self.page + 1)
        
        # Update the button states
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.total_pages - 1
        
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
    
    @discord.ui.button(label="Download", style=discord.ButtonStyle.primary)
    async def download_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Download the current document."""
        document = self.documents[self.page]
        doc_id = document["docid"]
        
        # Get the cog
        cog = interaction.client.get_cog("DMSCommands")
        if cog:
            # Call the download command
            await cog.download_document_slash(interaction, doc_id)
        else:
            await interaction.response.send_message("Error: Could not find the DMS commands cog.", ephemeral=True)


async def setup(bot: commands.Bot):
    """Add the DMS commands cog to the bot."""
    await bot.add_cog(DMSCommands(bot))
